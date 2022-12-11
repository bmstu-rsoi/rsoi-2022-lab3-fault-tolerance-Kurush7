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
-- Name: rating; Type: TABLE; Schema: public; Owner: program
--

CREATE TABLE public.rating (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    stars integer NOT NULL,
    CONSTRAINT rating_stars_check CHECK (((stars >= 0) AND (stars <= 100)))
);


ALTER TABLE public.rating OWNER TO program;

--
-- Name: rating_id_seq; Type: SEQUENCE; Schema: public; Owner: program
--

CREATE SEQUENCE public.rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rating_id_seq OWNER TO program;

--
-- Name: rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: program
--

ALTER SEQUENCE public.rating_id_seq OWNED BY public.rating.id;


--
-- Name: rating id; Type: DEFAULT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.rating ALTER COLUMN id SET DEFAULT nextval('public.rating_id_seq'::regclass);


--
-- Data for Name: rating; Type: TABLE DATA; Schema: public; Owner: program
--

COPY public.rating (id, username, stars) FROM stdin;
1	kurush	70
2	Test Max	52
\.


--
-- Name: rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: program
--

SELECT pg_catalog.setval('public.rating_id_seq', 1, true);


--
-- Name: rating rating_pkey; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

