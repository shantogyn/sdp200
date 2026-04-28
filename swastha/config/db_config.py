# sob service file ekhane theke DB connection nebe

import mysql.connector  # MySQL er sathe connect korar jonno
from mysql.connector import Error  # connection error handle korar jonno


# ekhane MySQL server er detail
DB_CONFIG = {
    "host":     "localhost",   
    "user":     "root",         
    "password": "",         
    "database": "swastha_db", 
    "charset":  "utf8mb4",     
}


def get_connection():
    """
    MySQL database e connection create kore return kore.
    Jodi connection fail kore, None return kore.
    eita sob service file theke call kora hobe.
    """
    try:
        # db_config use kore MySQL e connect korar cheshta
        conn = mysql.connector.connect(**DB_CONFIG)

        if conn.is_connected():
            return conn  # successful connection return 

    except Error as e:
        # connection fail 
        print(f"[DB ERROR] Database connection fail hoyeche: {e}")
        return None


def close_connection(conn):
    """
    Database connection band kore dey.
    Memory leak theke bachate sob kaj sesh hole ei function call korte hobe.
    """
    if conn and conn.is_connected():
        conn.close()  # connection close kora hocche


def init_database():
 
    try:
        # prothome database chara connect koro
        init_conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            charset=DB_CONFIG["charset"]
        )

        cursor = init_conn.cursor()

        # database na thakle create koro
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )

        cursor.execute(f"USE {DB_CONFIG['database']}")

        # ====== TABLE CREATION ======

        # users table — login/signup er jonno
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(256) NOT NULL,
                email    VARCHAR(150),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # reminders table — medicine reminder er jonno
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                user_id       INT NOT NULL,
                medicine_name VARCHAR(150) NOT NULL,
                reminder_time TIME NOT NULL,
                is_active     TINYINT(1) DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # reports table — lab report text save er jonno
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                user_id     INT NOT NULL,
                report_text LONGTEXT,
                uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # diseases table — disease info er jonno
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                name        VARCHAR(150) UNIQUE NOT NULL,
                symptoms    TEXT,
                causes      TEXT,
                prevention  TEXT,
                treatment   TEXT,
                description TEXT
            )
        """)

        # diet_plans table — diet recommendation er jonno
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diet_plans (
                id             INT AUTO_INCREMENT PRIMARY KEY,
                disease        VARCHAR(150) NOT NULL,
                recommendation TEXT NOT NULL
            )
        """)

        # alerts table — health alert system er jonno
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id           INT AUTO_INCREMENT PRIMARY KEY,
                location     VARCHAR(200) NOT NULL,
                disease_name VARCHAR(150) NOT NULL,
                severity     ENUM('Low','Medium','High') DEFAULT 'Medium',
                description  TEXT,
                created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        init_conn.commit()  

       
        _insert_sample_data(cursor, init_conn)

        cursor.close()
        init_conn.close()
        print("[DB] Database successfully initialized!")

    except Error as e:
        print(f"[DB ERROR] Database initialize korte somossa: {e}")


def _insert_sample_data(cursor, conn):
    """
    Prothombar database setup er somoy sample diseases, diet plans
    ar alerts insert kore — testing er jonno.
    """
   
    sample_diseases = [
        (
            "Diabetes",
            "Frequent urination, excessive thirst, blurred vision, fatigue",
            "Insulin resistance, genetic factors, obesity, sedentary lifestyle",
            "Healthy diet, regular exercise, weight management, avoid sugar",
            "Insulin therapy, oral medications, lifestyle changes, blood sugar monitoring",
            "Diabetes is a chronic disease where blood sugar levels are too high."
        ),
        (
            "Hypertension",
            "Headache, dizziness, chest pain, shortness of breath",
            "Stress, high salt intake, obesity, genetics, lack of exercise",
            "Reduce salt, exercise daily, avoid stress, no smoking",
            "ACE inhibitors, beta blockers, diuretics, lifestyle changes",
            "Hypertension or high blood pressure is a major risk factor for heart disease."
        ),
        (
            "Dengue",
            "High fever, severe headache, joint pain, rash, vomiting",
            "Aedes mosquito bite carrying dengue virus",
            "Use mosquito nets, repellents, eliminate stagnant water",
            "Hydration, rest, paracetamol for fever, platelet monitoring",
            "Dengue fever is a viral infection transmitted by Aedes mosquitoes."
        ),
        (
            "Common Cold",
            "Runny nose, sore throat, cough, mild fever, sneezing",
            "Rhinovirus, weakened immunity, cold weather exposure",
            "Wash hands frequently, avoid close contact with infected",
            "Rest, fluids, antihistamines, decongestants",
            "Common cold is a mild viral infection of the upper respiratory tract."
        ),
        (
            "Typhoid",
            "High fever, stomach pain, headache, weakness, diarrhea",
            "Salmonella typhi bacteria through contaminated water or food",
            "Safe drinking water, proper sanitation, typhoid vaccine",
            "Antibiotics (ciprofloxacin), rest, hydration",
            "Typhoid is a bacterial infection caused by Salmonella typhi."
        ),
    ]

    for d in sample_diseases:
        cursor.execute("""
            INSERT IGNORE INTO diseases
            (name, symptoms, causes, prevention, treatment, description)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, d)

  
    sample_diets = [
        ("Diabetes",     "Avoid sugar, eat whole grains, leafy vegetables. Drink plenty of water. Small frequent meals. Avoid processed food."),
        ("Hypertension", "Low sodium diet, eat fruits and vegetables, reduce red meat. Include potassium-rich foods like bananas. Avoid caffeine."),
        ("Dengue",       "High fluid intake, coconut water, papaya leaf juice, light meals. Avoid solid heavy food during fever."),
        ("Common Cold",  "Warm soups, ginger tea, vitamin C rich foods like orange and lemon. Stay hydrated. Avoid cold food."),
        ("Typhoid",      "Soft cooked foods, bananas, boiled potatoes. Avoid raw vegetables. High calorie diet for recovery."),
    ]

    for dp in sample_diets:
        cursor.execute(
            "INSERT IGNORE INTO diet_plans (disease, recommendation) VALUES (%s,%s)",
            dp
        )


    sample_alerts = [
        ("Dhaka, Bangladesh",    "Dengue",      "High",   "Dengue outbreak reported in multiple areas. Avoid mosquito bites."),
        ("Chittagong, Bangladesh","Typhoid",     "Medium", "Typhoid cases rising due to contaminated water supply."),
        ("Sylhet, Bangladesh",   "Diarrhea",    "Low",    "Mild increase in diarrhea cases. Drink safe water."),
        ("Rajshahi, Bangladesh", "Hypertension","Medium", "High BP cases increasing. Health camps being organized."),
    ]

    for al in sample_alerts:
        cursor.execute(
            "INSERT IGNORE INTO alerts (location, disease_name, severity, description) VALUES (%s,%s,%s,%s)",
            al
        )

    conn.commit() 