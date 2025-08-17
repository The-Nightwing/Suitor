
CREATE TABLE User (
  userID char(10),
  password char(8),
   CHECK (length(password) = 8),
  PRIMARY KEY (userID)
);

create table clients(
	userID char(10) NOT NULL,
    PRIMARY KEY (userID),
    FOREIGN KEY (userID) REFERENCES User(userID)
);

CREATE TABLE Opposition (
  oppositionID char(10) NOT NULL,
  firstName varchar(30) NOT NULL,
  middleName varchar(30) DEFAULT NULL,
  lastName varchar(30) NOT NULL,
  emailID varchar(256) NOT NULL,
  phoneNumber char(10) NOT NULL,
  streetName varchar(256) NOT NULL,
  city varchar(50) NOT NULL,
  pincode varchar(10) NOT NULL,
  state varchar(50) NOT NULL,

  PRIMARY KEY (oppositionID)
);


CREATE TABLE LegalCases (
  caseID char(15) NOT NULL,
  plaintiff varchar(256) NOT NULL,
  lastDateOfActivity date NOT NULL,
  flair varchar(256) NOT NULL,
  dateOfFiling date NOT NULL,
  duration mediumint NOT NULL,
  status varchar(256),
  PRIMARY KEY (caseID),
  CHECK (status IN ("Won","Active","Lost","Settled"))
);

CREATE TABLE FinancialTransactions (
  transactionID char(10) NOT NULL,
  dateOfPayment date NOT NULL,
  description varchar(256) default NULL,
  amount mediumint NOT NULL,
  type tinyint NOT NULL,
  PRIMARY KEY (transactionID),
  CHECK (amount!=0),
  CHECK (type=0 OR type= 1)
);

CREATE TABLE 'Calendar' (
  userID char(10) NOT NULL,
  whentt datetime not null,
  description varchar(256) default NULL,
  PRIMARY KEY ('userID','whentt'),
   FOREIGN KEY ('userID') REFERENCES 'User'('userID')
);

CREATE TABLE ClientCompanies (
  userID char(10) NOT NULL,
  firstName varchar(30) NOT NULL,
  middleName varchar(30) default NULL,
  lastName varchar(30) NOT NULL,
  budget mediumint NOT NULL,
  emailID varchar(256) NOT NULL,
  phoneNumber char(10) NOT NULL,
  streetName varchar(256) NOT NULL,
  city varchar(50) NOT NULL,
  pincode varchar(10) NOT NULL,
  state varchar(50) NOT NULL,
  isClient tinyint NOT NULL,
  fax varchar(100) default NULL,
  companyName varchar(256) NOT NULL,
  gstIN varchar(11) default NULL,

  PRIMARY KEY (userID),
  foreign key (userID) references clients(userID)
);

CREATE TABLE CourtHearing (
  caseID char(15) NOT NULL,
  nextHearingDate date default NULL,
  courtRoom varchar(256) NOT NULL,
  time time NOT NULL,
  PRIMARY KEY (caseID,time),
  FOREIGN KEY (caseID) REFERENCES LegalCases(caseID),
  CHECK (time > "09:00" AND time< "19:00")
);

CREATE TABLE IndividualClients (
  userID char(10) NOT NULL,
  firstName varchar(30) NOT NULL,
  middleName varchar(30) default NULL,
  lastName varchar(30) NOT NULL,
  dateOfBirth date NOT NULL,
  budget mediumint NOT NULL,
  emailID varchar(256) NOT NULL,
  phoneNumber char(10) NOT NULL,
  streetName varchar(256) NOT NULL,
  city varchar(50) NOT NULL,
  pincode varchar(10) NOT NULL,
  state varchar(50) NOT NULL,
  isClient tinyint NOT NULL,
  PRIMARY KEY (userID),
foreign key (userID) references clients(userID),
  CHECK (budget!=0),
  CHECK (isClient=1 or isClient= 0)
);


CREATE TABLE Lawyer (
  userID char(10) NOT NULL,
  firstName varchar(30) NOT NULL,
  middleName varchar(30) DEFAULT NULL,
  lastName varchar(30) NOT NULL,

  dateOfBirth date NOT NULL,
  gender varchar(30) NOT NULL,

  charges mediumint NOT NULL,
  casesWon mediumint NOT NULL,
  casesLost mediumint NOT NULL,
  casesSettled mediumint NOT NULL,
  experience mediumint NOT NULL,

  emailID varchar(256) NOT NULL,
  phoneNumber char(10) NOT NULL,
  positionAtFirm varchar(100) NOT NULL,

  avgTimePerCase mediumint NOT NULL,
  streetName varchar(256) NOT NULL,
  city varchar(50) NOT NULL,
  pincode varchar(10) NOT NULL,
  state varchar(50) NOT NULL,
  specialization varchar(256) NOT NULL,
  clientRating mediumint NOT NULL,

  PRIMARY KEY (userID,specialization),
  FOREIGN KEY (userID) REFERENCES User(userID),
  CHECK (clientRating>=0 AND clientRating<=10),
  CHECK (positionAtFirm IN ("Lawyer","Associate","Paralegal","Partner")),
  CHECK (charges>=2000 AND charges <= 20000)
);


CREATE TABLE LegalDocuments (
 
  docID char(10) NOT NULL,
  caseID char(15) NOT NULL,
  createdOn date NOT NULL,
  dateLastModified date NOT NULL,
  visibility tinyint NOT NULL,
  type varchar(256) NOT NULL,

  PRIMARY KEY (docID,caseID),
  FOREIGN KEY (caseID) REFERENCES LegalCases(caseID),
  check(visibility=0 or visibility= 1)
  
);



CREATE TABLE OtherStaff (
  userID char(10) NOT NULL,
  firstName varchar(30) NOT NULL,
  middleName varchar(30) DEFAULT NULL,
  lastName varchar(30) NOT NULL,
  dateOfBirth date NOT NULL,
  gender varchar(30) NOT NULL,
  salary mediumint NOT NULL,
  experience mediumint NOT NULL,
  emailID varchar(256) NOT NULL,
  phoneNumber char(10) NOT NULL,
  positionAtFirm varchar(100) NOT NULL,
  streetName varchar(256) NOT NULL,
  city varchar(50) NOT NULL,
  pincode varchar(10) NOT NULL,
  state varchar(50) NOT NULL,

  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES User(userID),
  CHECK (positionAtFirm IN ("HR","PR","Finance and Accounting","IT","Support Staff")),
  CHECK (salary>=2000 AND salary <= 20000)
);

CREATE TABLE Against (
  oppositionID char(10) NOT NULL,
  caseID char(15) NOT NULL,
  PRIMARY KEY (oppositionID,caseID),
  FOREIGN KEY (oppositionID) REFERENCES Opposition(oppositionID),
  FOREIGN KEY (caseID) REFERENCES LegalCases(caseID)
);

CREATE TABLE 'DisplayedIn' (
  'caseID' char(15) NOT NULL,
  'whentt' datetime NOT NULL,
  'userID' char(10) not null,
  PRIMARY KEY ('caseID','whentt','userID'),
  -- foreign key ('whentt') references 'Calendar'('whentt'),
  foreign key ('userID','whentt') references 'Calendar'('userID','whentt'),
  foreign key ('caseID') references 'LegalCases'('caseID')
);

CREATE TABLE Handles (
  userID char(10) NOT NULL,
  caseID char(15) NOT NULL,
  PRIMARY KEY (userID,caseID),
  foreign key (userID) references Lawyer(userID),
  foreign key (caseID) references LegalCases(caseID)
);

CREATE TABLE HasA (
  userID char(10) NOT NULL,
  caseID char(15) NOT NULL,
   PRIMARY KEY (userID,caseID),
   foreign key (userID) references clients(userID),
  foreign key (caseID) references LegalCases(caseID)
);

CREATE TABLE Invest (
  transactionID char(10) NOT NULL,
  caseID char(15) NOT NULL,
  PRIMARY KEY (transactionID,caseID),
  foreign key (caseID) references LegalCases(caseID),
  foreign key (transactionID) references FinancialTransactions(transactionID)
);


CREATE TABLE Makes (
  userID char(10) NOT NULL,
  transactionID char(10) NOT NULL,
  PRIMARY KEY (userID,transactionID),
  foreign key (userID) references User(userID),
  foreign key (transactionID) references FinancialTransactions(transactionID)
);