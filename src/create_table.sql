-- Table: public.covid19_stats

-- DROP TABLE public.covid19_stats;

CREATE TABLE public.covid19_stats
(
    id integer NOT NULL,
    txt_date text COLLATE pg_catalog."default",
    state text COLLATE pg_catalog."default",
    fips text COLLATE pg_catalog."default",
    positive integer,
    negative integer,
    total_tests integer,
    hospitalized integer,
    deaths integer,
    infect_rate real,
    hosp_rate real,
    death_rate real,
    CONSTRAINT id_pk PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.covid19_stats
    OWNER to postgres;