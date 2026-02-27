CREATE TABLE "USUARIOS" (
  "PK_id_usuario" int PRIMARY KEY,
  "FK_id_rol" int,
  "email" varchar,
  "password" varchar,
  "estado" bool,
  "fecha_registro" date
);

CREATE TABLE "ROLES" (
  "PK_id_rol" int PRIMARY KEY,
  "nombre_rol" varchar
);

CREATE TABLE "PERSONAS" (
  "PK_id_persona" int PRIMARY KEY,
  "FK_id_usuario" int UNIQUE,
  "nombres" varchar,
  "apellidos" varchar,
  "ci" varchar,
  "telefono" varchar,
  "foto_perfil" varchar,
  "semestre" int,
  "habilidades" text,
  "experiencia_prev" text
);

CREATE TABLE "EMPRESAS" (
  "PK_id_empresa" int PRIMARY KEY,
  "FK_id_usuario" int UNIQUE,
  "FK_id_sector" int,
  "nombre_comercial" varchar,
  "nit" varchar,
  "persona_contacto" varchar,
  "logo_empresa" varchar,
  "ubicacion" varchar,
  "descripcion_empresa" text
);

CREATE TABLE "SECTORES" (
  "PK_id_sector" int PRIMARY KEY,
  "nombre_sector" varchar
);

CREATE TABLE "CARRERAS" (
  "PK_id_persona_carrera" int PRIMARY KEY,
  "nombre_carrera" varchar
);

CREATE TABLE "PERSONAS_CARRERAS" (
  "FK_id_persona" int,
  "FK_id_carrera" int,
  "fecha_vinculacion" date,
  "estado_academico" varchar,
  PRIMARY KEY ("FK_id_persona", "FK_id_carrera")
);

CREATE TABLE "OFERTAS" (
  "PK_id_oferta" int PRIMARY KEY,
  "FK_id_empresa" int,
  "titulo" varchar,
  "descripcion" text,
  "requisitos" text,
  "fecha_limite" date,
  "estado" bool
);

CREATE TABLE "OFERTAS_CARRERAS" (
  "FK_id_oferta" int,
  "FK_id_carrera" int,
  PRIMARY KEY ("FK_id_oferta", "FK_id_carrera")
);

CREATE TABLE "POSTULACIONES" (
  "PK_id_postulacion" int PRIMARY KEY,
  "FK_id_persona" int,
  "FK_id_oferta" int,
  "mensaje_solicitud" text,
  "fecha_postulacion" date,
  "estado_proceso" varchar
);

ALTER TABLE "PERSONAS_CARRERAS" ADD FOREIGN KEY ("FK_id_persona") REFERENCES "PERSONAS" ("PK_id_persona");

ALTER TABLE "PERSONAS_CARRERAS" ADD FOREIGN KEY ("FK_id_carrera") REFERENCES "CARRERAS" ("PK_id_persona_carrera");

ALTER TABLE "OFERTAS_CARRERAS" ADD FOREIGN KEY ("FK_id_oferta") REFERENCES "OFERTAS" ("PK_id_oferta");

ALTER TABLE "OFERTAS_CARRERAS" ADD FOREIGN KEY ("FK_id_carrera") REFERENCES "CARRERAS" ("PK_id_persona_carrera");

ALTER TABLE "USUARIOS" ADD FOREIGN KEY ("FK_id_rol") REFERENCES "ROLES" ("PK_id_rol");

ALTER TABLE "USUARIOS" ADD FOREIGN KEY ("PK_id_usuario") REFERENCES "PERSONAS" ("FK_id_usuario");

ALTER TABLE "USUARIOS" ADD FOREIGN KEY ("PK_id_usuario") REFERENCES "EMPRESAS" ("FK_id_usuario");

ALTER TABLE "EMPRESAS" ADD FOREIGN KEY ("FK_id_sector") REFERENCES "SECTORES" ("PK_id_sector");

ALTER TABLE "OFERTAS" ADD FOREIGN KEY ("FK_id_empresa") REFERENCES "EMPRESAS" ("PK_id_empresa");

ALTER TABLE "POSTULACIONES" ADD FOREIGN KEY ("FK_id_persona") REFERENCES "PERSONAS" ("PK_id_persona");

ALTER TABLE "POSTULACIONES" ADD FOREIGN KEY ("FK_id_oferta") REFERENCES "OFERTAS" ("PK_id_oferta");
