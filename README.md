# wantek
Aplikasi POS dan Management Gudang untuk toko sepatu Wantek  

Link static file: https://drive.google.com/drive/folders/1DgYKyruf--Nr827usVi4iNZYBwMdOqSF?usp=drive_link  
Copy file static didalam folder wantek/ selevel dengan folder controllers, dao, models, others dan templates

DDL:  
CREATE TABLE roles (
	r_id varchar(2) NOT NULL,
	r_desc varchar(50) NULL,
	r_ins_date timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta'::text),
	r_ins_user varchar(20) NOT NULL,
	r_upd_date timestamp NULL,
	r_upd_user varchar(20) NULL,
	CONSTRAINT roles_pk PRIMARY KEY (r_id)
);  
INSERT INTO roles (r_id, r_desc, r_ins_date, r_ins_user, r_upd_date, r_upd_user) VALUES('00', 'Super user', '2023-12-05 22:34:20.179', 'benny', NULL, NULL);

CREATE TABLE users (
	u_username varchar(20) NOT NULL,
	u_password varchar(200) NOT NULL,
	u_role varchar(2) NOT NULL,
	u_status varchar(1) NOT NULL,
	u_ins_date timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta'::text),
	u_ins_user varchar(20) NOT NULL,
	u_upd_date timestamp NULL,
	u_upd_user varchar(20) NULL,
	CONSTRAINT users_pk PRIMARY KEY (u_username),
	CONSTRAINT users_fk FOREIGN KEY (u_role) REFERENCES roles(r_id)
);  
INSERT INTO users (u_username, u_password, u_role, u_status, u_ins_date, u_ins_user, u_upd_date, u_upd_user) VALUES('admin', 'e8ce2705794619658b2c544c846df56c', '00', 'T', '2023-12-05 19:43:18.365', 'admin', NULL, NULL);
