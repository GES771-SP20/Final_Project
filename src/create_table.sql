-- Table: public.covid19_stats

-- DROP TABLE public.covid19_stats;

CREATE TABLE public.covid19_stats
(
    id integer NOT NULL DEFAULT nextval('covid19_stats_id_seq'::regclass),
    "txtDate" text COLLATE pg_catalog."default",
    state text COLLATE pg_catalog."default",
    fips text COLLATE pg_catalog."default",
    positive integer,
    negative integer,
    "totalTests" integer,
    hospitalized integer,
    deaths integer,
    "infectRate" real,
    "hospRate" real,
    "deathRate" real,
    CONSTRAINT covid19_stats_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.covid19_stats
    OWNER to postgres;