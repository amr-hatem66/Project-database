create database Hotel_DB;
use Hotel_DB;
create table Guest(
Guest_Id int primary key,
Fname varchar(10) not null,
Lname varchar(10) not null,
phone varchar(15) not null,
Address  varchar(30),
sex varchar(6) not null,
Email varchar(30)
);
create table Booking(
Booking_Id int primary key,
Check_In_Date date not null,
Check_Out_Date date not null,
Booking_Status varchar(10) ,
Guest_Id int,
Room_Id int,
constraint Guest_Booking foreign key (Guest_Id) references Guest(Guest_Id),
constraint check_date check (Check_Out_Date>Check_In_Date),
constraint Booking_Room foreign key (Room_Id) references Room(Room_Id)
);
create table Room (
Room_Id int primary key,
Room_Number numeric(5) unique not null,
Room_Type varchar(15) not null,
price_per_night numeric(5) not null,
Availability_Status varchar(20) not null,
constraint price_check check(price_per_night>0)
);
create table bill(
Bill_Id int primary key,
Total_Amount numeric (8) not null,
Payment_Status varchar(10),
Payment_Method varchar(10) default 'cash',
book_Id int,
constraint Bill_Book foreign key (book_Id) references booking(booking_id),
constraint Check_PaymentStatus CHECK (Payment_Status IN ('Paid', 'Pending'))
);
create table Servicess(
Service_Id int primary key ,
Service_Name varchar(20) not null,
cost numeric(6) not null
);
create table Bill_Service(
Discount numeric(5),
Bill_Id int,
Service_Id int,
constraint Bill_constain foreign key (Bill_Id) references bill(bill_id),
constraint service_constain foreign key (service_Id) references servicess(service_id),
constraint s1 primary key( Bill_Id,Service_Id)
);

alter table booking
alter column  Check_In_Date varchar(20);

alter table booking
alter column  Check_out_Date varchar(20);

