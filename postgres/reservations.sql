--
-- PostgreSQL database dump
--

-- Dumped from database version 13.8 (Debian 13.8-1.pgdg110+1)
-- Dumped by pg_dump version 13.8 (Debian 13.8-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: reservation; Type: TABLE; Schema: public; Owner: program
--

CREATE TABLE public.reservation (
    id integer NOT NULL,
    reservation_uid uuid NOT NULL,
    username character varying(80) NOT NULL,
    book_uid uuid NOT NULL,
    library_uid uuid NOT NULL,
    status character varying(20) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    till_date timestamp without time zone NOT NULL,
    CONSTRAINT reservation_status_check CHECK (((status)::text = ANY ((ARRAY['RENTED'::character varying, 'RETURNED'::character varying, 'EXPIRED'::character varying])::text[])))
);


ALTER TABLE public.reservation OWNER TO program;

--
-- Name: reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: program
--

CREATE SEQUENCE public.reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reservation_id_seq OWNER TO program;

--
-- Name: reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: program
--

ALTER SEQUENCE public.reservation_id_seq OWNED BY public.reservation.id;


--
-- Name: reservation id; Type: DEFAULT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.reservation ALTER COLUMN id SET DEFAULT nextval('public.reservation_id_seq'::regclass);


--
-- Data for Name: reservation; Type: TABLE DATA; Schema: public; Owner: program
--

COPY public.reservation (id, reservation_uid, username, book_uid, library_uid, status, start_date, till_date) FROM stdin;
1	83575e12-7ce0-48ee-1111-51919ff3c9ee	kurush	f7cdc58f-2caf-4b15-9727-f89dcc629b27	83575e12-7ce0-48ee-9931-51919ff3c9ee	RENTED	2022-10-10 22:10:36	2022-10-20 22:10:43
12	47e42b4d-3bcb-4644-ac53-f4806f75ac86	kurush	f7cdc58f-2caf-4b15-9888-f89dcc629b27	83575e12-7ce0-48ee-9931-51919ff3c9ee	EXPIRED	2022-10-22 22:14:08.054341	2021-12-11 00:00:00
13	dd076280-0aab-4548-9f89-e3ad867db75f	Test Max	f7cdc58f-2caf-4b15-9727-f89dcc629b27	83575e12-7ce0-48ee-9931-51919ff3c9ee	RETURNED	2022-10-28 19:33:59.347646	2021-10-11 00:00:00
14	20993e24-e1ec-4433-bd51-8e5f2f2ad987	Test Max	f7cdc58f-2caf-4b15-9727-f89dcc629b27	83575e12-7ce0-48ee-9931-51919ff3c9ee	RETURNED	2022-10-28 19:37:31.973466	2021-10-11 00:00:00
\.


--
-- Name: reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: program
--

SELECT pg_catalog.setval('public.reservation_id_seq', 14, true);


--
-- Name: reservation reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_pkey PRIMARY KEY (id);


--
-- Name: reservation reservation_reservation_uid_key; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_reservation_uid_key UNIQUE (reservation_uid);


--
-- PostgreSQL database dump complete
--

