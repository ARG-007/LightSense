DROP DATABASE IF EXISTS LightSense;

CREATE DATABASE LightSense;

USE LightSense;

CREATE TABLE State (
    id INT PRIMARY KEY,
    value VARCHAR(10)
);

CREATE TABLE StreetLight (
    id INT PRIMARY KEY AUTO_INCREMENT,
    state INT DEFAULT 1,
    coords POINT,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (state) REFERENCES State(id)
);

CREATE TABLE Technician (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20),
    password VARCHAR(20)
) AUTO_INCREMENT = 1000;

CREATE TABLE Repair_Assignment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    light_id INT NOT NULL,
    assigned_to INT NOT NULL,
    assigned_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    task_state VARCHAR(10) DEFAULT "ASSIGNED",

    FOREIGN KEY (light_id) REFERENCES StreetLight(id),
    FOREIGN KEY (assigned_to) REFERENCES Technician(id),
    INDEX Light_and_taskstate (light_id, task_state),
    INDEX technician_and_taskstate (assigned_to, task_state),
    INDEX task_state (task_state)
);

CREATE TABLE SensorData (
    sensor_id INT,
    state INT,
    lamp_reading INT,
    env_reading INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sensor_id) REFERENCES StreetLight(id),
    FOREIGN KEY (state) REFERENCES State(id)
);

DELIMITER |
CREATE TRIGGER streetligt_update BEFORE INSERT ON SensorData 
FOR EACH ROW
BEGIN
UPDATE StreetLight SET updated_on=NEW.timestamp, state=NEW.state WHERE id = NEW.sensor_id;
END |

CREATE PROCEDURE Assign_Technician_With_MinWork(IN light_id INT)
BEGIN
    INSERT INTO Repair_Assignment(assigned_to, light_id) VALUE(
        (
            SELECT t.id FROM Technician t 
            LEFT JOIN Repair_Assignment rt ON t.id = rt.assigned_to AND task_state='ASSIGNED' 
            GROUP BY t.id 
            ORDER BY COUNT(*) 
            LIMIT 1),
        light_id );
END |

DELIMITER ;

INSERT INTO State VALUES 
(1, "WORKING"),
(2, "SLEEPING"),
(3, "FAULT");

INSERT INTO StreetLight(coords) VALUES
(POINT(11.55483427,78.01969886)),
(POINT(11.55474462,78.01970609)),
(POINT(11.55465497,78.01971331)),
(POINT(11.55456532,78.01972054)),
(POINT(11.55447566,78.01972777)),
(POINT(11.55438601,78.019735)),
(POINT(11.55429636,78.01974223)),
(POINT(11.5542067,78.01974946)),
(POINT(11.55411705,78.01975668)),
(POINT(11.55403099,78.01973004)),
(POINT(11.55394493,78.01970339)),
(POINT(11.55385887,78.01967675)),
(POINT(11.55377281,78.0196501)),
(POINT(11.55368675,78.01962346)),
(POINT(11.55360069,78.01959681)),
(POINT(11.55351463,78.01957017)),
(POINT(11.55342857,78.01954352)),
(POINT(11.55334251,78.01951688)),
(POINT(11.55325645,78.01949023)),
(POINT(11.55317039,78.01946358)),
(POINT(11.55308433,78.01943694)),
(POINT(11.55299827,78.01941029)),
(POINT(11.55291221,78.01938365)),
(POINT(11.55282647,78.01935595));

INSERT INTO Technician(name, password) VALUES 
("Gokul Kuttymani","11111"), 
("Dandabani Deepesh","22222"), 
("Shakthi Balaji","33333"), 
("Alagapuram Arun","44444");


