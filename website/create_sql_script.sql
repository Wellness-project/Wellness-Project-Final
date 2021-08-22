--Paste and execute this into your SQL script to create the database and a table

CREATE DATABASE journal;
USE journal;

create table mood_tracker(
tracker_date date not null,
happiness int not null,
 fitness int not null,
 sleep int not null,
 nutrition int not null,
 confidence int not null
);

select * from mood_tracker;