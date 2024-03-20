DROP DATABASE IF EXISTS cs122a;
CREATE DATABASE cs122a;
USE cs122a;

DROP TABLE IF EXISTS users, machines, courses;
CREATE TABLE users(
    UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
    FirstName VARCHAR(50),
    MiddleName VARCHAR(50),
    LastName VARCHAR(50)
);


CREATE TABLE machines(
    MachineID INT PRIMARY KEY NOT NULL,
    Hostname VARCHAR(255),
    IPAddress VARCHAR(15),
    OperationalStatus VARCHAR(50),
    Location VARCHAR(255)
);

CREATE TABLE courses(
    CourseID INT PRIMARY KEY NOT NULL,
    Title VARCHAR(100),
    Quarter VARCHAR(20)
);

CREATE TABLE userEmail (
    UCINetID VARCHAR(20) NOT NULL,
    Email VARCHAR(100),
    PRIMARY KEY (UCINetID, Email),
    FOREIGN KEY (UCINetID) REFERENCES users (UCINetID)
    ON DELETE CASCADE
);


CREATE TABLE students (
   UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
   FOREIGN KEY (UCINetID) REFERENCES users(UCINetID)
     ON DELETE CASCADE
);

CREATE TABLE administrators (
   UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
   FOREIGN KEY (UCINetID) REFERENCES users(UCINetID)
     ON DELETE CASCADE
);

CREATE TABLE projects (
   ProjectID INT PRIMARY KEY NOT NULL,
   Name VARCHAR(100),
   Description TEXT,
   CourseID INT NOT NULL,
   FOREIGN KEY (CourseID) REFERENCES courses(CourseID)
);


CREATE TABLE studentUse (
   ProjectID INT,
   StudentUCINetID VARCHAR(20),
   MachineID INT,
   StartDate DATE,
   EndDate DATE,
   PRIMARY KEY (ProjectID, StudentUCINetID, MachineID),
   FOREIGN KEY (ProjectID) REFERENCES projects(ProjectID),
   FOREIGN KEY (StudentUCINetID) REFERENCES students(UCINetID),
   FOREIGN KEY (MachineID) REFERENCES machines(MachineID)
);


CREATE TABLE adminManageMachines (
   AdminUCINetID VARCHAR(20),
   MachineID INT,
   PRIMARY KEY (AdminUCINetID, MachineID),
   FOREIGN KEY (AdminUCINetID) REFERENCES administrators(UCINetID),
   FOREIGN KEY (MachineID) REFERENCES machines(MachineID)
);
