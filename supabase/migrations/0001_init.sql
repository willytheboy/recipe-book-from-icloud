create extension if not exists vector;
create extension if not exists pgcrypto;

create table photos (
  id uuid primary key default gen_random_uuid(),
  path text unique not null,
  sha256 text unique not null,
  taken_at timestamptz,
  width int, height int,
  is_food boolean,
  coarse_category text,
  dish text, cuisine text, category text,
  ingredients text[],
  cooking_method text,
  plating_context text,
  confidence numeric,
  visual_embedding vector(1024),
  cluster_id uuid,
  is_primary boolean default false,
  gphotos_media_id text,
  gphotos_product_url text,
  created_at timestamptz default now()
);
create index on photos using ivfflat (visual_embedding vector_cosine_ops) with (lists=100);
create index on photos (is_food) where is_food = true;
create index on photos (cluster_id);

create table clusters (
  id uuid primary key default gen_random_uuid(),
  label text, cuisine text, category text,
  hero_photo_id uuid references photos(id),
  size int, album_id text, album_title text
);

create table recipes (
  cluster_id uuid primary key references clusters(id) on delete cascade,
  title text, ingredients_md text, steps_md text, notes_md text,
  generated_by text,
  created_at timestamptz default now()
);
