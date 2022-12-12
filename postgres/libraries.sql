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
-- Name: books; Type: TABLE; Schema: public; Owner: program
--

CREATE TABLE public.books (
    id integer NOT NULL,
    book_uid uuid NOT NULL,
    name character varying(255) NOT NULL,
    author character varying(255),
    genre character varying(255),
    condition character varying(20) DEFAULT 'EXCELLENT'::character varying,
    CONSTRAINT books_condition_check CHECK (((condition)::text = ANY ((ARRAY['EXCELLENT'::character varying, 'GOOD'::character varying, 'BAD'::character varying])::text[])))
);


ALTER TABLE public.books OWNER TO program;

--
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: program
--

CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.books_id_seq OWNER TO program;

--
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: program
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- Name: library; Type: TABLE; Schema: public; Owner: program
--

CREATE TABLE public.library (
    id integer NOT NULL,
    library_uid uuid NOT NULL,
    name character varying(80) NOT NULL,
    city character varying(255) NOT NULL,
    address character varying(255) NOT NULL
);


ALTER TABLE public.library OWNER TO program;

--
-- Name: library_books; Type: TABLE; Schema: public; Owner: program
--

CREATE TABLE public.library_books (
    book_id integer,
    library_id integer,
    available_count integer NOT NULL
);


ALTER TABLE public.library_books OWNER TO program;

--
-- Name: library_id_seq; Type: SEQUENCE; Schema: public; Owner: program
--

CREATE SEQUENCE public.library_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.library_id_seq OWNER TO program;

--
-- Name: library_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: program
--

ALTER SEQUENCE public.library_id_seq OWNED BY public.library.id;


--
-- Name: books id; Type: DEFAULT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- Name: library id; Type: DEFAULT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.library ALTER COLUMN id SET DEFAULT nextval('public.library_id_seq'::regclass);


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: program
--

COPY public.books (id, book_uid, name, author, genre, condition) FROM stdin;
1	f7cdc58f-2caf-4b15-9727-f89dcc629b27	Краткий курс C++ в 7 томах	Бьерн Страуструп	Научная фантастика	EXCELLENT
2	f7cdc58f-2caf-4b15-9888-f89dcc629b27	Длинный курс C++ в 7 томах	Бьерн Страуструп	Научная фантастика	EXCELLENT
\.


--
-- Data for Name: library; Type: TABLE DATA; Schema: public; Owner: program
--

COPY public.library (id, library_uid, name, city, address) FROM stdin;
1	83575e12-7ce0-48ee-9931-51919ff3c9ee	Библиотека имени 7 Непьющих	Москва	2-я Бауманская ул., д.5, стр.1
\.


--
-- Data for Name: library_books; Type: TABLE DATA; Schema: public; Owner: program
--

COPY public.library_books (book_id, library_id, available_count) FROM stdin;
2	1	91
1	1	1
\.


--
-- Name: books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: program
--

SELECT pg_catalog.setval('public.books_id_seq', 2, true);


--
-- Name: library_id_seq; Type: SEQUENCE SET; Schema: public; Owner: program
--

SELECT pg_catalog.setval('public.library_id_seq', 1, true);


--
-- Name: books books_book_uid_key; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_book_uid_key UNIQUE (book_uid);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);


--
-- Name: library library_library_uid_key; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_library_uid_key UNIQUE (library_uid);


--
-- Name: library library_pkey; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_pkey PRIMARY KEY (id);


--
-- Name: library_books library_books_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.library_books
    ADD CONSTRAINT library_books_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id);


--
-- Name: library_books library_books_library_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.library_books
    ADD CONSTRAINT library_books_library_id_fkey FOREIGN KEY (library_id) REFERENCES public.library(id);


--
-- PostgreSQL database dump complete
--

