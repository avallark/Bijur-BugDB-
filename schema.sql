drop table if exists users;

create table users (
    user_id INTEGER NOT NULL AUTO_INCREMENT, 
    email_id char(100) not null,  
    password char(60) not null, 
    user_name char(50),     
    status char(1) default 'A',
    PRIMARY KEY (user_id) 
);

-- Legend Status : A - Active , I - Inactive
-- password : currently set to iese1234 by default.

drop table if exists m_debug;

create table m_debug (
   text text
);

drop table if exists bug_header;

create table bug_header(
   bug_id INTEGER not null auto_increment,
   bug_title text not null,
   bug_description text,
   assigned_to_user_id integer,
   customer char(10),
   status char(10),
   priority integer,
   last_updated_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   primary key (bug_id)
);

-- legend 
-- status = OPEN, CLOSED, ESCAL, WAIT

drop table if exists bug_body;

create table bug_body(
   bug_body_id integer not null auto_increment,
   bug_id integer,
   bug_update text,
   last_updated_time timestamp DEFAULT CURRENT_TIMESTAMP,
   updated_by integer,
   primary key (bug_body_id)
);

drop table if exists all_status;

create table all_status(
   status char(10),
   status_Description text,
   primary key (status)
);

 -- Setting some default statuses, you can edit them from /status while running the app.                
insert into all_status values ('OPEN','The bug is open and pending resolution from developer');
insert into all_status values ('WAIT','The bug is open and awaiting response from user');
insert into all_status values ('CLOSED','The bug has been closed');
insert into all_status values ('SUSPENDED','The bug has been suspended and will be opened later');
insert into all_status values ('ITWAIT','The bug is waiting for other department in IT');

drop table if exists categories;

create table categories(
   category_id integer not null auto_increment,
   category_name char(15) not null,
   category_description char(50),
   parent_Category_id integer,
   category_owner_id integer,
   primary key (category_id)
);



