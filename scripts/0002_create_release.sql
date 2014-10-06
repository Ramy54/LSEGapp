create table release (
	id varchar(255) not null primary key,
	git_branch varchar(255),
	commit_date varchar(80),
	author varchar(255),
	support_works_number varchar(8)
)