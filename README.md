# wantek
Aplikasi POS dan Management Gudang untuk toko sepatu Wantek  

Link static file: https://drive.google.com/drive/folders/1DgYKyruf--Nr827usVi4iNZYBwMdOqSF?usp=drive_link  
Copy file static didalam folder wantek/ selevel dengan folder controllers, dao, models, others dan templates

DDL:  
CREATE TABLE roles (
	r_id varchar(2) NOT NULL,
	r_desc varchar(30) NULL,
	r_ins_date timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta'::text),
	r_ins_user varchar(20) NOT NULL,
	r_upd_date timestamp NULL,
	r_upd_user varchar(20) NULL,
	r_status varchar(1) NULL,
	CONSTRAINT roles_pk PRIMARY KEY (r_id)
);  
INSERT INTO roles (r_id, r_desc, r_ins_date, r_ins_user, r_upd_date, r_upd_user, r_status) VALUES('00', 'Super user', '2023-12-17 21:51:46.960', 'root', '2023-12-18 01:13:40.199', 'benny', 'T');

CREATE TABLE cabang (
	c_id varchar(4) NOT NULL,
	c_desc varchar(100) NULL,
	c_ins_date timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta'::text),
	c_ins_user varchar(20) NOT NULL,
	c_upd_date timestamp NULL,
	c_upd_user varchar(20) NULL,
	c_status varchar(1) NOT NULL,
	c_alamat varchar(200) NULL,
	CONSTRAINT cabang_pk PRIMARY KEY (c_id)
);  
INSERT INTO cabang (c_id, c_desc, c_ins_date, c_ins_user, c_upd_date, c_upd_user, c_aktif, c_alamat) VALUES('P001', 'PARAKAN', '2023-12-17 16:56:41.820', 'benny', NULL, NULL, 'T', NULL);

CREATE TABLE menus (
	m_id varchar(4) NOT NULL,
	m_desc varchar(200) NOT NULL,
	m_parent varchar(4) NULL,
	m_link varchar(200) NULL,
	m_ins_date timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta'::text),
	m_ins_user varchar(20) NOT NULL,
	m_upd_date time NULL,
	m_upd_user varchar(20) NULL,
	CONSTRAINT menus_pk PRIMARY KEY (m_id)
);  
INSERT INTO menus (m_id, m_desc, m_parent, m_link, m_ins_date, m_ins_user, m_upd_date, m_upd_user) VALUES('0-01', 'Master user', '0-00', '/master/user', '2023-12-13 00:00:36.502', 'benny', NULL, NULL);  
INSERT INTO menus (m_id, m_desc, m_parent, m_link, m_ins_date, m_ins_user, m_upd_date, m_upd_user) VALUES('0-02', 'Master role', '0-00', '/master/role', '2023-12-13 00:00:36.503', 'benny', NULL, NULL);  
INSERT INTO menus (m_id, m_desc, m_parent, m_link, m_ins_date, m_ins_user, m_upd_date, m_upd_user) VALUES('2-00', 'Report', NULL, '/report', '2023-12-13 00:01:00.711', 'benny', NULL, NULL);  
INSERT INTO menus (m_id, m_desc, m_parent, m_link, m_ins_date, m_ins_user, m_upd_date, m_upd_user) VALUES('1-00', 'Transaksi', NULL, '/transaksi', '2023-12-13 00:00:36.504', 'benny', NULL, NULL);  
INSERT INTO menus (m_id, m_desc, m_parent, m_link, m_ins_date, m_ins_user, m_upd_date, m_upd_user) VALUES('0-00', 'Master', NULL, NULL, '2023-12-13 00:00:36.500', 'benny', NULL, NULL);  

CREATE TABLE access_menu (
	am_r_id varchar(20) NOT NULL,
	am_m_id varchar(4) NOT NULL,
	am_upd_user varchar(20) NOT NULL,
	am_upd_date timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta'::text),
	CONSTRAINT access_menu_pk PRIMARY KEY (am_r_id, am_m_id),
	CONSTRAINT access_menu_fk FOREIGN KEY (am_r_id) REFERENCES roles(r_id),
	CONSTRAINT access_menu_fk_1 FOREIGN KEY (am_m_id) REFERENCES menus(m_id)
);  
INSERT INTO access_menu (am_r_id, am_m_id, am_upd_user, am_upd_date) VALUES('00', '0-00', 'benny', '2023-12-17 21:52:48.946');  
INSERT INTO access_menu (am_r_id, am_m_id, am_upd_user, am_upd_date) VALUES('00', '0-01', 'benny', '2023-12-17 21:52:48.947');  
INSERT INTO access_menu (am_r_id, am_m_id, am_upd_user, am_upd_date) VALUES('00', '0-02', 'benny', '2023-12-17 21:52:48.948');  
INSERT INTO access_menu (am_r_id, am_m_id, am_upd_user, am_upd_date) VALUES('00', '1-00', 'benny', '2023-12-17 21:52:48.949');  
INSERT INTO access_menu (am_r_id, am_m_id, am_upd_user, am_upd_date) VALUES('00', '2-00', 'benny', '2023-12-17 21:52:48.949');  

CREATE TABLE users (
	u_username varchar(20) NOT NULL,
	u_password varchar(200) NOT NULL,
	u_role varchar(2) NOT NULL,
	u_status varchar(1) NOT NULL,
	u_ins_date timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta'::text),
	u_ins_user varchar(20) NOT NULL,
	u_upd_date timestamp NULL,
	u_upd_user varchar(20) NULL,
	u_cabang varchar(4) NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (u_username),
	CONSTRAINT users_cabang_fk FOREIGN KEY (u_cabang) REFERENCES cabang(c_id),
	CONSTRAINT users_fk FOREIGN KEY (u_role) REFERENCES roles(r_id)
);  
INSERT INTO users (u_username, u_password, u_role, u_status, u_ins_date, u_ins_user, u_upd_date, u_upd_user, u_cabang) VALUES('benny', 'e8ce2705794619658b2c544c846df56c', '00', 'T', '2023-12-17 21:52:08.906', 'root', NULL, NULL, 'P001');
