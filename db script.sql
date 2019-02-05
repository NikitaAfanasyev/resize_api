create table resizejobs(
	jobid serial,
	status character varying(30),
    height int,
    width int,
    imagename character varying(50),
	creationDate timestamp DEFAULT ('now'::text)::timestamp
);


insert into resizeJobs (status, height, width) values ('done', 5, 6);
