create table deployment (
	id int not null primary key GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1),
	host_id varchar(255) not null,
	release_id varchar(255) not null,
	previous_release_id varchar(255),
	install_time varchar(40) not null,
	duration double not null,
	install_path varchar(255) not null,
	puppetmaster varchar(32) not null,
	constraint host_fk foreign key (host_id) references host (hostname),
	constraint release_fk foreign key (release_id) references release (id)
)