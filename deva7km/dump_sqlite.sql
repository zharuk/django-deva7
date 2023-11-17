--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.4 в Чт ноя 16 22:20:13 2023
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: auth_group
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

-- Таблица: auth_group_permissions
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Таблица: auth_permission
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (1, 1, 'add_logentry', 'Can add log entry');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (2, 1, 'change_logentry', 'Can change log entry');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (3, 1, 'delete_logentry', 'Can delete log entry');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (4, 1, 'view_logentry', 'Can view log entry');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (5, 2, 'add_permission', 'Can add permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (6, 2, 'change_permission', 'Can change permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (7, 2, 'delete_permission', 'Can delete permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (8, 2, 'view_permission', 'Can view permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (9, 3, 'add_group', 'Can add group');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (10, 3, 'change_group', 'Can change group');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (11, 3, 'delete_group', 'Can delete group');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (12, 3, 'view_group', 'Can view group');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (13, 4, 'add_user', 'Can add user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (14, 4, 'change_user', 'Can change user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (15, 4, 'delete_user', 'Can delete user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (16, 4, 'view_user', 'Can view user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (17, 5, 'add_contenttype', 'Can add content type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (18, 5, 'change_contenttype', 'Can change content type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (19, 5, 'delete_contenttype', 'Can delete content type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (20, 5, 'view_contenttype', 'Can view content type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (21, 6, 'add_session', 'Can add session');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (22, 6, 'change_session', 'Can change session');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (23, 6, 'delete_session', 'Can delete session');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (24, 6, 'view_session', 'Can view session');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (25, 7, 'add_product', 'Can add Товар');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (26, 7, 'change_product', 'Can change Товар');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (27, 7, 'delete_product', 'Can delete Товар');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (28, 7, 'view_product', 'Can view Товар');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (29, 8, 'add_productmodification', 'Can add Модификация товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (30, 8, 'change_productmodification', 'Can change Модификация товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (31, 8, 'delete_productmodification', 'Can delete Модификация товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (32, 8, 'view_productmodification', 'Can view Модификация товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (33, 9, 'add_category', 'Can add Категория товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (34, 9, 'change_category', 'Can change Категория товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (35, 9, 'delete_category', 'Can delete Категория товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (36, 9, 'view_category', 'Can view Категория товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (37, 10, 'add_image', 'Can add Изображение товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (38, 10, 'change_image', 'Can change Изображение товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (39, 10, 'delete_image', 'Can delete Изображение товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (40, 10, 'view_image', 'Can view Изображение товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (41, 11, 'add_color', 'Can add Цвет');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (42, 11, 'change_color', 'Can change Цвет');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (43, 11, 'delete_color', 'Can delete Цвет');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (44, 11, 'view_color', 'Can view Цвет');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (45, 12, 'add_size', 'Can add Размер');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (46, 12, 'change_size', 'Can change Размер');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (47, 12, 'delete_size', 'Can delete Размер');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (48, 12, 'view_size', 'Can view Размер');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (49, 13, 'add_sale', 'Can add Продажа');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (50, 13, 'change_sale', 'Can change Продажа');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (51, 13, 'delete_sale', 'Can delete Продажа');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (52, 13, 'view_sale', 'Can view Продажа');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (53, 14, 'add_saleitem', 'Can add Элемент продажи');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (54, 14, 'change_saleitem', 'Can change Элемент продажи');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (55, 14, 'delete_saleitem', 'Can delete Элемент продажи');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (56, 14, 'view_saleitem', 'Can view Элемент продажи');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (57, 15, 'add_return', 'Can add Возврат');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (58, 15, 'change_return', 'Can change Возврат');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (59, 15, 'delete_return', 'Can delete Возврат');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (60, 15, 'view_return', 'Can view Возврат');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (61, 16, 'add_returnitem', 'Can add Элемент возврата');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (62, 16, 'change_returnitem', 'Can change Элемент возврата');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (63, 16, 'delete_returnitem', 'Can delete Элемент возврата');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (64, 16, 'view_returnitem', 'Can view Элемент возврата');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (65, 17, 'add_stock', 'Can add Остаток товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (66, 17, 'change_stock', 'Can change Остаток товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (67, 17, 'delete_stock', 'Can delete Остаток товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (68, 17, 'view_stock', 'Can view Остаток товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (69, 18, 'add_telegramuser', 'Can add telegram user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (70, 18, 'change_telegramuser', 'Can change telegram user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (71, 18, 'delete_telegramuser', 'Can delete telegram user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (72, 18, 'view_telegramuser', 'Can view telegram user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (73, 19, 'add_inventory', 'Can add Оприходование');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (74, 19, 'change_inventory', 'Can change Оприходование');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (75, 19, 'delete_inventory', 'Can delete Оприходование');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (76, 19, 'view_inventory', 'Can view Оприходование');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (77, 20, 'add_inventoryitem', 'Can add Элемент оприходования');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (78, 20, 'change_inventoryitem', 'Can change Элемент оприходования');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (79, 20, 'delete_inventoryitem', 'Can delete Элемент оприходования');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (80, 20, 'view_inventoryitem', 'Can view Элемент оприходования');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (81, 21, 'add_writeoff', 'Can add Списание товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (82, 21, 'change_writeoff', 'Can change Списание товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (83, 21, 'delete_writeoff', 'Can delete Списание товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (84, 21, 'view_writeoff', 'Can view Списание товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (85, 22, 'add_writeoffitem', 'Can add Элемент списания товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (86, 22, 'change_writeoffitem', 'Can change Элемент списания товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (87, 22, 'delete_writeoffitem', 'Can delete Элемент списания товара');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (88, 22, 'view_writeoffitem', 'Can view Элемент списания товара');

-- Таблица: auth_user
CREATE TABLE IF NOT EXISTS "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);
INSERT INTO auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) VALUES (1, 'pbkdf2_sha256$600000$g9lfBO8zoISzn8fOTQPx2J$kJ2EBjVg8pAKS5VQ/towLHE6KpAYThswa7A722fknE0=', '2023-11-11 09:59:41.912519', 1, 'zharuk', '', '', 1, 1, '2023-10-28 09:50:35.189026', '');

-- Таблица: auth_user_groups
CREATE TABLE IF NOT EXISTS "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Таблица: auth_user_user_permissions
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Таблица: catalog_category
CREATE TABLE IF NOT EXISTS "catalog_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "created_at" datetime NOT NULL, "slug" varchar(200) NOT NULL UNIQUE);
INSERT INTO catalog_category (id, name, created_at, slug) VALUES (1, 'Платья', '2023-10-28 09:52:40.756161', 'platia');
INSERT INTO catalog_category (id, name, created_at, slug) VALUES (2, 'Боди', '2023-10-29 09:22:28.209947', 'bodi');
INSERT INTO catalog_category (id, name, created_at, slug) VALUES (3, 'Костюмы', '2023-10-29 13:48:27.527943', 'kostiumy');
INSERT INTO catalog_category (id, name, created_at, slug) VALUES (4, 'Юбки', '2023-10-30 20:28:26.316883', 'iubki');
INSERT INTO catalog_category (id, name, created_at, slug) VALUES (5, 'Блузки', '2023-10-31 17:33:06.824078', 'bluzki');
INSERT INTO catalog_category (id, name, created_at, slug) VALUES (6, 'Штаны', '2023-11-16 19:22:18.639047', 'shtany');

-- Таблица: catalog_color
CREATE TABLE IF NOT EXISTS "catalog_color" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE);
INSERT INTO catalog_color (id, name) VALUES (1, 'белый');
INSERT INTO catalog_color (id, name) VALUES (2, 'красный');
INSERT INTO catalog_color (id, name) VALUES (3, 'черный');
INSERT INTO catalog_color (id, name) VALUES (4, 'беж');
INSERT INTO catalog_color (id, name) VALUES (5, 'меланж');
INSERT INTO catalog_color (id, name) VALUES (6, 'бутылка');
INSERT INTO catalog_color (id, name) VALUES (7, 'темно-синий');
INSERT INTO catalog_color (id, name) VALUES (8, 'мокко');
INSERT INTO catalog_color (id, name) VALUES (9, 'малина');
INSERT INTO catalog_color (id, name) VALUES (10, 'синий');
INSERT INTO catalog_color (id, name) VALUES (11, 'молоко');
INSERT INTO catalog_color (id, name) VALUES (12, 'голубой');
INSERT INTO catalog_color (id, name) VALUES (13, 'шоколад');
INSERT INTO catalog_color (id, name) VALUES (14, 'горчица');
INSERT INTO catalog_color (id, name) VALUES (15, 'хаки');

-- Таблица: catalog_image
CREATE TABLE IF NOT EXISTS "catalog_image" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "image" varchar(100) NOT NULL, "modification_id" bigint NOT NULL REFERENCES "catalog_productmodification" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_image (id, image, modification_id) VALUES (19, 'images/photo_2023-10-29_11-23-46.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (20, 'images/photo_2023-10-29_11-23-43.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (21, 'images/photo_2023-10-29_11-23-39.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (22, 'images/photo_2023-10-29_11-23-30.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (23, 'images/photo_2023-10-29_12-03-39.jpg', 32);
INSERT INTO catalog_image (id, image, modification_id) VALUES (24, 'images/photo_2023-10-29_12-03-37.jpg', 32);
INSERT INTO catalog_image (id, image, modification_id) VALUES (25, 'images/photo_2023-10-29_12-03-34.jpg', 32);
INSERT INTO catalog_image (id, image, modification_id) VALUES (26, 'images/photo_2023-10-29_12-03-26.jpg', 32);
INSERT INTO catalog_image (id, image, modification_id) VALUES (27, 'images/photo_2023-10-29_12-03-39_ZdwjBTp.jpg', 31);
INSERT INTO catalog_image (id, image, modification_id) VALUES (28, 'images/photo_2023-10-29_12-03-37_9X7BaMg.jpg', 31);
INSERT INTO catalog_image (id, image, modification_id) VALUES (29, 'images/photo_2023-10-29_12-03-34_iSwMsFr.jpg', 31);
INSERT INTO catalog_image (id, image, modification_id) VALUES (30, 'images/photo_2023-10-29_12-03-26_NOnzQJQ.jpg', 31);
INSERT INTO catalog_image (id, image, modification_id) VALUES (31, 'images/photo_2023-10-29_12-09-06_dYfQMmd.jpg', 34);
INSERT INTO catalog_image (id, image, modification_id) VALUES (32, 'images/photo_2023-10-29_12-09-03.jpg', 34);
INSERT INTO catalog_image (id, image, modification_id) VALUES (33, 'images/photo_2023-10-29_12-09-01.jpg', 34);
INSERT INTO catalog_image (id, image, modification_id) VALUES (34, 'images/photo_2023-10-29_12-08-57.jpg', 34);
INSERT INTO catalog_image (id, image, modification_id) VALUES (35, 'images/photo_2023-10-29_12-08-43.jpg', 34);
INSERT INTO catalog_image (id, image, modification_id) VALUES (36, 'images/photo_2023-10-29_12-09-06_kOLUaGl.jpg', 34);
INSERT INTO catalog_image (id, image, modification_id) VALUES (37, 'images/photo_2023-10-29_12-09-06_JFS7OkF.jpg', 34);
INSERT INTO catalog_image (id, image, modification_id) VALUES (38, 'images/photo_2023-10-29_12-09-06_Ct0pYLy.jpg', 34);
INSERT INTO catalog_image (id, image, modification_id) VALUES (48, 'images/photo_2023-10-29_12-09-06_ixynaBQ.jpg', 33);
INSERT INTO catalog_image (id, image, modification_id) VALUES (49, 'images/photo_2023-10-29_12-09-03_moI04FJ.jpg', 33);
INSERT INTO catalog_image (id, image, modification_id) VALUES (50, 'images/photo_2023-10-29_12-09-01_7R07UK1.jpg', 33);
INSERT INTO catalog_image (id, image, modification_id) VALUES (51, 'images/photo_2023-10-29_12-08-57_vsF1jAb.jpg', 33);
INSERT INTO catalog_image (id, image, modification_id) VALUES (52, 'images/photo_2023-10-29_12-08-43_bAKSbbQ.jpg', 33);
INSERT INTO catalog_image (id, image, modification_id) VALUES (59, 'images/photo_2023-10-29_15-19-14_nNXL9ry.jpg', 40);
INSERT INTO catalog_image (id, image, modification_id) VALUES (60, 'images/photo_2023-10-29_15-19-14_nNXL9ry.jpg', 39);
INSERT INTO catalog_image (id, image, modification_id) VALUES (61, 'images/photo_2023-10-29_15-19-10_2izkK9X.jpg', 40);
INSERT INTO catalog_image (id, image, modification_id) VALUES (62, 'images/photo_2023-10-29_15-19-10_2izkK9X.jpg', 39);
INSERT INTO catalog_image (id, image, modification_id) VALUES (63, 'images/photo_2023-10-29_15-19-07_QNI5IKW.jpg', 40);
INSERT INTO catalog_image (id, image, modification_id) VALUES (64, 'images/photo_2023-10-29_15-19-07_QNI5IKW.jpg', 39);
INSERT INTO catalog_image (id, image, modification_id) VALUES (65, 'images/photo_2023-10-29_15-19-04_oBPuPmn.jpg', 40);
INSERT INTO catalog_image (id, image, modification_id) VALUES (66, 'images/photo_2023-10-29_15-19-04_oBPuPmn.jpg', 39);
INSERT INTO catalog_image (id, image, modification_id) VALUES (67, 'images/photo_2023-10-29_15-18-56_9jthBef.jpg', 40);
INSERT INTO catalog_image (id, image, modification_id) VALUES (70, 'images/photo_2023-10-29_15-18-56_h3lPz5f.jpg', 39);
INSERT INTO catalog_image (id, image, modification_id) VALUES (71, 'images/photo_2023-10-29_15-49-16.jpg', 41);
INSERT INTO catalog_image (id, image, modification_id) VALUES (72, 'images/photo_2023-10-29_15-49-13.jpg', 41);
INSERT INTO catalog_image (id, image, modification_id) VALUES (73, 'images/photo_2023-10-29_15-49-10.jpg', 41);
INSERT INTO catalog_image (id, image, modification_id) VALUES (74, 'images/photo_2023-10-29_15-49-08.jpg', 41);
INSERT INTO catalog_image (id, image, modification_id) VALUES (75, 'images/photo_2023-10-29_15-48-58.jpg', 41);
INSERT INTO catalog_image (id, image, modification_id) VALUES (76, 'images/photo_2023-10-29_15-54-47.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (77, 'images/photo_2023-10-29_15-54-45.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (78, 'images/photo_2023-10-29_15-54-42.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (79, 'images/photo_2023-10-29_15-54-40.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (80, 'images/photo_2023-10-29_15-54-38.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (81, 'images/photo_2023-10-29_15-54-35.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (82, 'images/photo_2023-10-29_15-54-32.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (83, 'images/photo_2023-10-29_15-54-30.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (84, 'images/photo_2023-10-29_15-54-21.jpg', 30);
INSERT INTO catalog_image (id, image, modification_id) VALUES (85, 'images/photo_2023-10-29_21-21-09.jpg', 44);
INSERT INTO catalog_image (id, image, modification_id) VALUES (86, 'images/photo_2023-10-29_21-21-04.jpg', 44);
INSERT INTO catalog_image (id, image, modification_id) VALUES (87, 'images/photo_2023-10-29_21-21-21.jpg', 43);
INSERT INTO catalog_image (id, image, modification_id) VALUES (88, 'images/photo_2023-10-29_21-21-15.jpg', 43);
INSERT INTO catalog_image (id, image, modification_id) VALUES (89, 'images/photo_2023-10-29_21-21-12.jpg', 43);
INSERT INTO catalog_image (id, image, modification_id) VALUES (90, 'images/photo_2023-10-29_21-21-23.jpg', 42);
INSERT INTO catalog_image (id, image, modification_id) VALUES (91, 'images/photo_2023-10-29_21-21-18.jpg', 42);
INSERT INTO catalog_image (id, image, modification_id) VALUES (92, 'images/photo_2023-10-29_21-21-07.jpg', 42);
INSERT INTO catalog_image (id, image, modification_id) VALUES (93, 'images/photo_2023-10-29_21-21-02.jpg', 42);
INSERT INTO catalog_image (id, image, modification_id) VALUES (94, 'images/photo_2023-10-29_21-20-52.jpg', 42);
INSERT INTO catalog_image (id, image, modification_id) VALUES (95, 'images/photo_2023-10-29_21-33-34.jpg', 50);
INSERT INTO catalog_image (id, image, modification_id) VALUES (96, 'images/photo_2023-10-29_21-33-34.jpg', 49);
INSERT INTO catalog_image (id, image, modification_id) VALUES (97, 'images/photo_2023-10-29_21-33-28.jpg', 50);
INSERT INTO catalog_image (id, image, modification_id) VALUES (98, 'images/photo_2023-10-29_21-33-28.jpg', 49);
INSERT INTO catalog_image (id, image, modification_id) VALUES (99, 'images/photo_2023-10-29_21-33-44.jpg', 48);
INSERT INTO catalog_image (id, image, modification_id) VALUES (100, 'images/photo_2023-10-29_21-33-44.jpg', 47);
INSERT INTO catalog_image (id, image, modification_id) VALUES (101, 'images/photo_2023-10-29_21-33-42.jpg', 48);
INSERT INTO catalog_image (id, image, modification_id) VALUES (102, 'images/photo_2023-10-29_21-33-42.jpg', 47);
INSERT INTO catalog_image (id, image, modification_id) VALUES (103, 'images/photo_2023-10-29_21-33-40.jpg', 48);
INSERT INTO catalog_image (id, image, modification_id) VALUES (104, 'images/photo_2023-10-29_21-33-40.jpg', 47);
INSERT INTO catalog_image (id, image, modification_id) VALUES (105, 'images/photo_2023-10-29_21-33-37.jpg', 48);
INSERT INTO catalog_image (id, image, modification_id) VALUES (106, 'images/photo_2023-10-29_21-33-37.jpg', 47);
INSERT INTO catalog_image (id, image, modification_id) VALUES (107, 'images/photo_2023-10-29_21-33-53.jpg', 46);
INSERT INTO catalog_image (id, image, modification_id) VALUES (108, 'images/photo_2023-10-29_21-33-53.jpg', 45);
INSERT INTO catalog_image (id, image, modification_id) VALUES (109, 'images/photo_2023-10-29_21-33-50.jpg', 46);
INSERT INTO catalog_image (id, image, modification_id) VALUES (110, 'images/photo_2023-10-29_21-33-50.jpg', 45);
INSERT INTO catalog_image (id, image, modification_id) VALUES (111, 'images/photo_2023-10-29_21-33-47.jpg', 46);
INSERT INTO catalog_image (id, image, modification_id) VALUES (112, 'images/photo_2023-10-29_21-33-47.jpg', 45);
INSERT INTO catalog_image (id, image, modification_id) VALUES (113, 'images/photo_2023-10-29_21-40-43.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (114, 'images/photo_2023-10-29_21-40-40.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (115, 'images/photo_2023-10-29_21-40-37.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (116, 'images/photo_2023-10-29_21-40-30.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (117, 'images/photo_2023-10-30_10-35-40.jpg', 53);
INSERT INTO catalog_image (id, image, modification_id) VALUES (118, 'images/photo_2023-10-30_10-35-40.jpg', 52);
INSERT INTO catalog_image (id, image, modification_id) VALUES (119, 'images/photo_2023-10-30_10-35-38.jpg', 53);
INSERT INTO catalog_image (id, image, modification_id) VALUES (120, 'images/photo_2023-10-30_10-35-38.jpg', 52);
INSERT INTO catalog_image (id, image, modification_id) VALUES (121, 'images/photo_2023-10-30_10-35-35.jpg', 53);
INSERT INTO catalog_image (id, image, modification_id) VALUES (122, 'images/photo_2023-10-30_10-35-35.jpg', 52);
INSERT INTO catalog_image (id, image, modification_id) VALUES (123, 'images/photo_2023-10-30_10-35-23.jpg', 53);
INSERT INTO catalog_image (id, image, modification_id) VALUES (124, 'images/photo_2023-10-30_10-35-23.jpg', 52);
INSERT INTO catalog_image (id, image, modification_id) VALUES (125, 'images/photo_2023-10-30_10-43-30.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (126, 'images/photo_2023-10-30_10-43-30.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (127, 'images/photo_2023-10-30_10-43-28.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (128, 'images/photo_2023-10-30_10-43-28.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (129, 'images/photo_2023-10-30_10-43-26.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (130, 'images/photo_2023-10-30_10-43-26.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (131, 'images/photo_2023-10-30_10-43-23.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (132, 'images/photo_2023-10-30_10-43-23.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (133, 'images/photo_2023-10-30_10-43-16.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (134, 'images/photo_2023-10-30_10-43-16.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (135, 'images/photo_2023-10-30_10-49-33.jpg', 56);
INSERT INTO catalog_image (id, image, modification_id) VALUES (136, 'images/photo_2023-10-30_10-49-30.jpg', 56);
INSERT INTO catalog_image (id, image, modification_id) VALUES (137, 'images/photo_2023-10-30_10-49-28.jpg', 56);
INSERT INTO catalog_image (id, image, modification_id) VALUES (138, 'images/photo_2023-10-30_10-49-25.jpg', 56);
INSERT INTO catalog_image (id, image, modification_id) VALUES (139, 'images/photo_2023-10-30_10-49-16.jpg', 56);
INSERT INTO catalog_image (id, image, modification_id) VALUES (140, 'images/photo_2023-10-30_12-10-21.jpg', 58);
INSERT INTO catalog_image (id, image, modification_id) VALUES (141, 'images/photo_2023-10-30_12-10-24.jpg', 58);
INSERT INTO catalog_image (id, image, modification_id) VALUES (142, 'images/photo_2023-10-30_12-10-26.jpg', 58);
INSERT INTO catalog_image (id, image, modification_id) VALUES (143, 'images/photo_2023-10-30_12-10-19.jpg', 57);
INSERT INTO catalog_image (id, image, modification_id) VALUES (144, 'images/photo_2023-10-30_12-10-12.jpg', 57);
INSERT INTO catalog_image (id, image, modification_id) VALUES (145, 'images/photo_2023-10-30_17-55-39.jpg', 60);
INSERT INTO catalog_image (id, image, modification_id) VALUES (146, 'images/photo_2023-10-30_17-55-39.jpg', 59);
INSERT INTO catalog_image (id, image, modification_id) VALUES (147, 'images/photo_2023-10-30_17-55-54.jpg', 60);
INSERT INTO catalog_image (id, image, modification_id) VALUES (148, 'images/photo_2023-10-30_17-55-54.jpg', 59);
INSERT INTO catalog_image (id, image, modification_id) VALUES (149, 'images/photo_2023-10-30_17-55-52.jpg', 60);
INSERT INTO catalog_image (id, image, modification_id) VALUES (150, 'images/photo_2023-10-30_17-55-52.jpg', 59);
INSERT INTO catalog_image (id, image, modification_id) VALUES (151, 'images/photo_2023-10-30_17-55-50.jpg', 60);
INSERT INTO catalog_image (id, image, modification_id) VALUES (152, 'images/photo_2023-10-30_17-55-50.jpg', 59);
INSERT INTO catalog_image (id, image, modification_id) VALUES (153, 'images/photo_2023-10-30_17-55-47.jpg', 60);
INSERT INTO catalog_image (id, image, modification_id) VALUES (154, 'images/photo_2023-10-30_17-55-47.jpg', 59);
INSERT INTO catalog_image (id, image, modification_id) VALUES (155, 'images/photo_2023-10-30_17-55-44.jpg', 60);
INSERT INTO catalog_image (id, image, modification_id) VALUES (156, 'images/photo_2023-10-30_17-55-44.jpg', 59);
INSERT INTO catalog_image (id, image, modification_id) VALUES (157, 'images/photo_2023-10-30_17-55-41.jpg', 60);
INSERT INTO catalog_image (id, image, modification_id) VALUES (158, 'images/photo_2023-10-30_17-55-41.jpg', 59);
INSERT INTO catalog_image (id, image, modification_id) VALUES (159, 'images/photo_2023-10-30_17-55-31.jpg', 60);
INSERT INTO catalog_image (id, image, modification_id) VALUES (160, 'images/photo_2023-10-30_17-55-31.jpg', 59);
INSERT INTO catalog_image (id, image, modification_id) VALUES (169, 'images/photo_2023-10-29_12-21-32.jpg', 36);
INSERT INTO catalog_image (id, image, modification_id) VALUES (170, 'images/photo_2023-10-29_12-21-32.jpg', 35);
INSERT INTO catalog_image (id, image, modification_id) VALUES (171, 'images/photo_2023-10-29_12-21-40.jpg', 36);
INSERT INTO catalog_image (id, image, modification_id) VALUES (172, 'images/photo_2023-10-29_12-21-40.jpg', 35);
INSERT INTO catalog_image (id, image, modification_id) VALUES (173, 'images/photo_2023-10-29_12-21-46.jpg', 36);
INSERT INTO catalog_image (id, image, modification_id) VALUES (174, 'images/photo_2023-10-29_12-21-46.jpg', 35);
INSERT INTO catalog_image (id, image, modification_id) VALUES (175, 'images/photo_2023-10-29_12-21-49.jpg', 36);
INSERT INTO catalog_image (id, image, modification_id) VALUES (176, 'images/photo_2023-10-29_12-21-49.jpg', 35);
INSERT INTO catalog_image (id, image, modification_id) VALUES (177, 'images/photo_2023-10-30_18-53-36.jpg', 61);
INSERT INTO catalog_image (id, image, modification_id) VALUES (178, 'images/photo_2023-10-30_18-53-45.jpg', 61);
INSERT INTO catalog_image (id, image, modification_id) VALUES (179, 'images/photo_2023-10-30_18-53-48.jpg', 62);
INSERT INTO catalog_image (id, image, modification_id) VALUES (180, 'images/photo_2023-10-30_18-53-51.jpg', 62);
INSERT INTO catalog_image (id, image, modification_id) VALUES (181, 'images/photo_2023-10-30_22-26-34.jpg', 65);
INSERT INTO catalog_image (id, image, modification_id) VALUES (182, 'images/photo_2023-10-30_22-26-52.jpg', 64);
INSERT INTO catalog_image (id, image, modification_id) VALUES (183, 'images/photo_2023-10-30_22-26-49.jpg', 64);
INSERT INTO catalog_image (id, image, modification_id) VALUES (184, 'images/photo_2023-10-30_22-26-41.jpg', 64);
INSERT INTO catalog_image (id, image, modification_id) VALUES (185, 'images/photo_2023-10-30_22-26-39.jpg', 64);
INSERT INTO catalog_image (id, image, modification_id) VALUES (186, 'images/photo_2023-10-30_22-26-54.jpg', 63);
INSERT INTO catalog_image (id, image, modification_id) VALUES (187, 'images/photo_2023-10-30_22-26-46.jpg', 63);
INSERT INTO catalog_image (id, image, modification_id) VALUES (188, 'images/photo_2023-10-30_22-26-44.jpg', 63);
INSERT INTO catalog_image (id, image, modification_id) VALUES (189, 'images/photo_2023-10-30_22-26-37.jpg', 63);
INSERT INTO catalog_image (id, image, modification_id) VALUES (190, 'images/photo_2023-10-30_22-29-06.jpg', 66);
INSERT INTO catalog_image (id, image, modification_id) VALUES (191, 'images/photo_2023-10-30_22-29-03.jpg', 66);
INSERT INTO catalog_image (id, image, modification_id) VALUES (192, 'images/photo_2023-10-30_22-53-09.jpg', 72);
INSERT INTO catalog_image (id, image, modification_id) VALUES (193, 'images/photo_2023-10-30_22-53-09.jpg', 71);
INSERT INTO catalog_image (id, image, modification_id) VALUES (194, 'images/photo_2023-10-30_22-53-07.jpg', 72);
INSERT INTO catalog_image (id, image, modification_id) VALUES (195, 'images/photo_2023-10-30_22-53-07.jpg', 71);
INSERT INTO catalog_image (id, image, modification_id) VALUES (196, 'images/photo_2023-10-30_22-53-05.jpg', 72);
INSERT INTO catalog_image (id, image, modification_id) VALUES (197, 'images/photo_2023-10-30_22-53-05.jpg', 71);
INSERT INTO catalog_image (id, image, modification_id) VALUES (198, 'images/photo_2023-10-30_22-53-02.jpg', 72);
INSERT INTO catalog_image (id, image, modification_id) VALUES (199, 'images/photo_2023-10-30_22-53-02.jpg', 71);
INSERT INTO catalog_image (id, image, modification_id) VALUES (200, 'images/photo_2023-10-30_22-52-54.jpg', 70);
INSERT INTO catalog_image (id, image, modification_id) VALUES (201, 'images/photo_2023-10-30_22-52-54.jpg', 69);
INSERT INTO catalog_image (id, image, modification_id) VALUES (202, 'images/photo_2023-10-30_22-52-57.jpg', 70);
INSERT INTO catalog_image (id, image, modification_id) VALUES (203, 'images/photo_2023-10-30_22-52-57.jpg', 69);
INSERT INTO catalog_image (id, image, modification_id) VALUES (204, 'images/photo_2023-10-30_22-52-59.jpg', 70);
INSERT INTO catalog_image (id, image, modification_id) VALUES (205, 'images/photo_2023-10-30_22-52-59.jpg', 69);
INSERT INTO catalog_image (id, image, modification_id) VALUES (206, 'images/photo_2023-10-30_22-52-52.jpg', 70);
INSERT INTO catalog_image (id, image, modification_id) VALUES (207, 'images/photo_2023-10-30_22-52-52.jpg', 69);
INSERT INTO catalog_image (id, image, modification_id) VALUES (208, 'images/photo_2023-10-30_22-52-49.jpg', 70);
INSERT INTO catalog_image (id, image, modification_id) VALUES (209, 'images/photo_2023-10-30_22-52-49.jpg', 69);
INSERT INTO catalog_image (id, image, modification_id) VALUES (210, 'images/photo_2023-10-30_22-52-39.jpg', 70);
INSERT INTO catalog_image (id, image, modification_id) VALUES (211, 'images/photo_2023-10-30_22-52-39.jpg', 69);
INSERT INTO catalog_image (id, image, modification_id) VALUES (212, 'images/photo_2023-10-30_22-52-20.jpg', 68);
INSERT INTO catalog_image (id, image, modification_id) VALUES (213, 'images/photo_2023-10-30_22-52-20.jpg', 67);
INSERT INTO catalog_image (id, image, modification_id) VALUES (214, 'images/photo_2023-10-30_22-52-26.jpg', 68);
INSERT INTO catalog_image (id, image, modification_id) VALUES (215, 'images/photo_2023-10-30_22-52-26.jpg', 67);
INSERT INTO catalog_image (id, image, modification_id) VALUES (216, 'images/photo_2023-10-30_22-52-28.jpg', 68);
INSERT INTO catalog_image (id, image, modification_id) VALUES (217, 'images/photo_2023-10-30_22-52-28.jpg', 67);
INSERT INTO catalog_image (id, image, modification_id) VALUES (218, 'images/photo_2023-10-30_22-52-30.jpg', 68);
INSERT INTO catalog_image (id, image, modification_id) VALUES (219, 'images/photo_2023-10-30_22-52-30.jpg', 67);
INSERT INTO catalog_image (id, image, modification_id) VALUES (220, 'images/photo_2023-10-30_22-52-33.jpg', 68);
INSERT INTO catalog_image (id, image, modification_id) VALUES (221, 'images/photo_2023-10-30_22-52-33.jpg', 67);
INSERT INTO catalog_image (id, image, modification_id) VALUES (222, 'images/photo_2023-10-30_22-52-35.jpg', 68);
INSERT INTO catalog_image (id, image, modification_id) VALUES (223, 'images/photo_2023-10-30_22-52-35.jpg', 67);
INSERT INTO catalog_image (id, image, modification_id) VALUES (224, 'images/photo_2023-10-31_19-34-02.jpg', 78);
INSERT INTO catalog_image (id, image, modification_id) VALUES (225, 'images/photo_2023-10-31_19-34-02.jpg', 77);
INSERT INTO catalog_image (id, image, modification_id) VALUES (226, 'images/photo_2023-10-31_19-34-14.jpg', 78);
INSERT INTO catalog_image (id, image, modification_id) VALUES (227, 'images/photo_2023-10-31_19-34-14.jpg', 77);
INSERT INTO catalog_image (id, image, modification_id) VALUES (228, 'images/photo_2023-10-31_19-34-17.jpg', 78);
INSERT INTO catalog_image (id, image, modification_id) VALUES (229, 'images/photo_2023-10-31_19-34-17.jpg', 77);
INSERT INTO catalog_image (id, image, modification_id) VALUES (230, 'images/photo_2023-10-31_19-34-22.jpg', 76);
INSERT INTO catalog_image (id, image, modification_id) VALUES (231, 'images/photo_2023-10-31_19-34-22.jpg', 75);
INSERT INTO catalog_image (id, image, modification_id) VALUES (232, 'images/photo_2023-10-31_19-34-19.jpg', 76);
INSERT INTO catalog_image (id, image, modification_id) VALUES (233, 'images/photo_2023-10-31_19-34-19.jpg', 75);
INSERT INTO catalog_image (id, image, modification_id) VALUES (234, 'images/photo_2023-11-02_21-22-48.jpg', 80);
INSERT INTO catalog_image (id, image, modification_id) VALUES (235, 'images/photo_2023-11-02_21-22-46.jpg', 80);
INSERT INTO catalog_image (id, image, modification_id) VALUES (236, 'images/photo_2023-11-02_21-22-43.jpg', 80);
INSERT INTO catalog_image (id, image, modification_id) VALUES (237, 'images/photo_2023-11-02_21-22-41.jpg', 80);
INSERT INTO catalog_image (id, image, modification_id) VALUES (238, 'images/photo_2023-11-02_21-22-39.jpg', 79);
INSERT INTO catalog_image (id, image, modification_id) VALUES (239, 'images/photo_2023-11-02_21-22-37.jpg', 79);
INSERT INTO catalog_image (id, image, modification_id) VALUES (240, 'images/photo_2023-11-02_21-22-34.jpg', 79);
INSERT INTO catalog_image (id, image, modification_id) VALUES (241, 'images/photo_2023-11-02_21-22-26.jpg', 79);
INSERT INTO catalog_image (id, image, modification_id) VALUES (242, 'images/photo_2023-11-03_21-13-32.jpg', 82);
INSERT INTO catalog_image (id, image, modification_id) VALUES (243, 'images/photo_2023-11-03_21-13-40.jpg', 82);
INSERT INTO catalog_image (id, image, modification_id) VALUES (244, 'images/photo_2023-11-03_21-13-43.jpg', 82);
INSERT INTO catalog_image (id, image, modification_id) VALUES (245, 'images/photo_2023-11-03_21-13-48.jpg', 81);
INSERT INTO catalog_image (id, image, modification_id) VALUES (246, 'images/photo_2023-11-03_21-13-45.jpg', 81);
INSERT INTO catalog_image (id, image, modification_id) VALUES (247, 'images/photo_2023-11-03_21-16-47.jpg', 83);
INSERT INTO catalog_image (id, image, modification_id) VALUES (248, 'images/photo_2023-11-03_21-16-44.jpg', 83);
INSERT INTO catalog_image (id, image, modification_id) VALUES (249, 'images/photo_2023-11-03_21-16-41.jpg', 83);
INSERT INTO catalog_image (id, image, modification_id) VALUES (250, 'images/photo_2023-11-03_21-20-57.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (251, 'images/photo_2023-11-03_21-20-57.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (252, 'images/photo_2023-11-03_21-20-55.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (253, 'images/photo_2023-11-03_21-20-55.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (254, 'images/photo_2023-11-03_21-20-53.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (255, 'images/photo_2023-11-03_21-20-53.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (256, 'images/photo_2023-11-03_21-20-45.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (257, 'images/photo_2023-11-03_21-20-45.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (258, 'images/photo_2023-11-06_20-40-16.jpg', 86);
INSERT INTO catalog_image (id, image, modification_id) VALUES (259, 'images/photo_2023-11-06_20-40-12.jpg', 86);
INSERT INTO catalog_image (id, image, modification_id) VALUES (260, 'images/photo_2023-11-11_12-00-35.jpg', 92);
INSERT INTO catalog_image (id, image, modification_id) VALUES (261, 'images/photo_2023-11-11_12-00-35.jpg', 91);
INSERT INTO catalog_image (id, image, modification_id) VALUES (262, 'images/photo_2023-11-11_12-00-37.jpg', 92);
INSERT INTO catalog_image (id, image, modification_id) VALUES (263, 'images/photo_2023-11-11_12-00-37.jpg', 91);
INSERT INTO catalog_image (id, image, modification_id) VALUES (264, 'images/photo_2023-11-11_12-00-30.jpg', 90);
INSERT INTO catalog_image (id, image, modification_id) VALUES (265, 'images/photo_2023-11-11_12-00-30.jpg', 89);
INSERT INTO catalog_image (id, image, modification_id) VALUES (266, 'images/photo_2023-11-11_12-00-32.jpg', 90);
INSERT INTO catalog_image (id, image, modification_id) VALUES (267, 'images/photo_2023-11-11_12-00-32.jpg', 89);
INSERT INTO catalog_image (id, image, modification_id) VALUES (268, 'images/photo_2023-11-11_12-00-19.jpg', 88);
INSERT INTO catalog_image (id, image, modification_id) VALUES (269, 'images/photo_2023-11-11_12-00-19.jpg', 87);
INSERT INTO catalog_image (id, image, modification_id) VALUES (270, 'images/photo_2023-11-11_12-00-27.jpg', 88);
INSERT INTO catalog_image (id, image, modification_id) VALUES (271, 'images/photo_2023-11-11_12-00-27.jpg', 87);
INSERT INTO catalog_image (id, image, modification_id) VALUES (272, 'images/photo_2023-11-15_21-54-10.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (273, 'images/photo_2023-11-15_21-54-07.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (274, 'images/photo_2023-11-15_21-54-04.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (275, 'images/photo_2023-11-15_21-54-02.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (276, 'images/photo_2023-11-15_21-53-59.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (277, 'images/photo_2023-11-15_21-53-56.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (278, 'images/photo_2023-11-15_21-53-53.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (279, 'images/photo_2023-11-15_21-53-50.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (280, 'images/photo_2023-11-15_21-53-48.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (281, 'images/photo_2023-11-15_21-53-38.jpg', 51);
INSERT INTO catalog_image (id, image, modification_id) VALUES (282, 'images/photo_2023-11-15_21-56-24.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (283, 'images/photo_2023-11-15_21-56-24.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (284, 'images/photo_2023-11-15_21-56-21.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (285, 'images/photo_2023-11-15_21-56-21.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (286, 'images/photo_2023-11-15_21-56-18.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (287, 'images/photo_2023-11-15_21-56-18.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (288, 'images/photo_2023-11-15_21-56-15.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (289, 'images/photo_2023-11-15_21-56-15.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (290, 'images/photo_2023-11-15_21-56-13.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (291, 'images/photo_2023-11-15_21-56-13.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (292, 'images/photo_2023-11-15_21-56-11.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (293, 'images/photo_2023-11-15_21-56-11.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (294, 'images/photo_2023-11-15_21-56-09.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (295, 'images/photo_2023-11-15_21-56-09.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (296, 'images/photo_2023-11-15_21-56-06.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (297, 'images/photo_2023-11-15_21-56-06.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (298, 'images/photo_2023-11-15_21-56-00.jpg', 85);
INSERT INTO catalog_image (id, image, modification_id) VALUES (299, 'images/photo_2023-11-15_21-56-00.jpg', 84);
INSERT INTO catalog_image (id, image, modification_id) VALUES (300, 'images/photo_2023-11-15_21-57-48.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (301, 'images/photo_2023-11-15_21-57-48.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (302, 'images/photo_2023-11-15_21-57-45.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (303, 'images/photo_2023-11-15_21-57-45.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (304, 'images/photo_2023-11-15_21-57-42.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (305, 'images/photo_2023-11-15_21-57-42.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (306, 'images/photo_2023-11-15_21-57-39.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (307, 'images/photo_2023-11-15_21-57-39.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (308, 'images/photo_2023-11-15_21-57-37.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (309, 'images/photo_2023-11-15_21-57-37.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (310, 'images/photo_2023-11-15_21-57-34.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (311, 'images/photo_2023-11-15_21-57-34.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (312, 'images/photo_2023-11-15_21-57-29.jpg', 55);
INSERT INTO catalog_image (id, image, modification_id) VALUES (313, 'images/photo_2023-11-15_21-57-29.jpg', 54);
INSERT INTO catalog_image (id, image, modification_id) VALUES (314, 'images/photo_2023-11-16_21-24-10.jpg', 98);
INSERT INTO catalog_image (id, image, modification_id) VALUES (315, 'images/photo_2023-11-16_21-24-10.jpg', 97);
INSERT INTO catalog_image (id, image, modification_id) VALUES (316, 'images/photo_2023-11-16_21-23-55.jpg', 98);
INSERT INTO catalog_image (id, image, modification_id) VALUES (317, 'images/photo_2023-11-16_21-23-55.jpg', 97);
INSERT INTO catalog_image (id, image, modification_id) VALUES (318, 'images/photo_2023-11-16_21-24-15.jpg', 96);
INSERT INTO catalog_image (id, image, modification_id) VALUES (319, 'images/photo_2023-11-16_21-24-15.jpg', 95);
INSERT INTO catalog_image (id, image, modification_id) VALUES (320, 'images/photo_2023-11-16_21-24-08.jpg', 96);
INSERT INTO catalog_image (id, image, modification_id) VALUES (321, 'images/photo_2023-11-16_21-24-08.jpg', 95);
INSERT INTO catalog_image (id, image, modification_id) VALUES (322, 'images/photo_2023-11-16_21-23-55_SlplJcQ.jpg', 96);
INSERT INTO catalog_image (id, image, modification_id) VALUES (323, 'images/photo_2023-11-16_21-23-55_SlplJcQ.jpg', 95);
INSERT INTO catalog_image (id, image, modification_id) VALUES (324, 'images/photo_2023-11-16_21-24-13.jpg', 94);
INSERT INTO catalog_image (id, image, modification_id) VALUES (325, 'images/photo_2023-11-16_21-24-13.jpg', 93);
INSERT INTO catalog_image (id, image, modification_id) VALUES (326, 'images/photo_2023-11-16_21-27-14.jpg', 100);
INSERT INTO catalog_image (id, image, modification_id) VALUES (327, 'images/photo_2023-11-16_21-27-14.jpg', 99);
INSERT INTO catalog_image (id, image, modification_id) VALUES (328, 'images/photo_2023-11-16_21-27-11.jpg', 100);
INSERT INTO catalog_image (id, image, modification_id) VALUES (329, 'images/photo_2023-11-16_21-27-11.jpg', 99);
INSERT INTO catalog_image (id, image, modification_id) VALUES (330, 'images/photo_2023-11-16_21-27-05.jpg', 100);
INSERT INTO catalog_image (id, image, modification_id) VALUES (331, 'images/photo_2023-11-16_21-27-05.jpg', 99);

-- Таблица: catalog_inventory
CREATE TABLE IF NOT EXISTS "catalog_inventory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "comment" text NOT NULL, "status" varchar(20) NOT NULL, "telegram_user_id" bigint NULL REFERENCES "catalog_telegramuser" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_inventory (id, created_at, comment, status, telegram_user_id, user_id) VALUES (6, '2023-11-16 08:44:22', '', 'completed', NULL, NULL);

-- Таблица: catalog_inventoryitem
CREATE TABLE IF NOT EXISTS "catalog_inventoryitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "inventory_id" bigint NOT NULL REFERENCES "catalog_inventory" ("id") DEFERRABLE INITIALLY DEFERRED, "product_modification_id" bigint NOT NULL REFERENCES "catalog_productmodification" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_inventoryitem (id, quantity, inventory_id, product_modification_id) VALUES (10, 3, 6, 85);
INSERT INTO catalog_inventoryitem (id, quantity, inventory_id, product_modification_id) VALUES (11, 2, 6, 78);

-- Таблица: catalog_product
CREATE TABLE IF NOT EXISTS "catalog_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "description" text NOT NULL, "sku" varchar(50) NOT NULL UNIQUE, "price" decimal NOT NULL, "currency" varchar(3) NOT NULL, "created_at" datetime NOT NULL, "category_id" bigint NOT NULL REFERENCES "catalog_category" ("id") DEFERRABLE INITIALLY DEFERRED, "is_active" bool NOT NULL, "updated_at" datetime NOT NULL, "slug" varchar(200) NOT NULL UNIQUE);
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (3, 'Боди черный', '?? Яка ж неймовірна краса ??
??Боді 
??Модель 1005 
??Ціна 250грн
??Тканина: мікро дайвінг (Хороша розтяжність)
 ??Колір:чорний 
??Розмір: 1(42-46) 

??Приголомшливий, сексуальний і мега класний боді ?? Сідає ідеально ?? Боді моделюючий фігуру ??', '1005', 250, 'UAH', '2023-10-29 09:23:07.468406', 2, 1, '2023-10-30 19:12:46.625144', 'bodi-chernyj-1005');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (4, 'Боди черный', '??Ось це новинка ??
 ??Боді 
??Модель 1004 
??Ціна 250грн 
??Тканина: Мікро дайвінг (хороша розтяжність)
 ??Колір:чорний ?? 
??Розміри: 1(42-46) 2(48-52) 
Ви тільки подивіться на цю красу ?? Боді в крутому виконанні ?? ідеально сидить і виглядає чарівно ??

Відправляємо на клієнта @Natadeva_7km', '1004', 250, 'UAH', '2023-10-29 09:58:21.923225', 2, 1, '2023-10-30 19:12:46.625144', 'bodi-chernyj-1004');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (5, 'Платье белое', '? ?????? ???????????????????? ?

?? Сукня

м. 1022
?? Розмір 42-44 і 46-48
??Тканина :мікро дайвінг
?? Колір :білий
?? Ціна 280грн 

Магія елегантності та жіночності зачарує вас, завдяки цьому облягаючой міні сукні!
 —————————
Довжина 85 см
42-44 ??
Грудь 82-88
Стегна 90-96

46-48 ??
Грудь 90-96
Стегна 98-104', '1022', 280, 'UAH', '2023-10-29 10:10:13.954626', 1, 1, '2023-10-30 19:12:46.625144', 'plate-beloe-1022');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (6, 'Платье с длинным рукавом', '??Знову у продажу ??
Сукня в стилі Oversize ??

?? Модель 411
?? Ціна 400грн
??Розміри 42-46 48-52
??Колір ?? чорний
?? Тканина
2х нитка та еко шкіра

Легка, зручна, вільна, красива сукня - в неї неможливо не закохатися??
Відправляємо на клієнта ?? @Natadeva_7km', '411', 400, 'UAH', '2023-10-29 10:22:37.717168', 1, 1, '2023-10-30 19:12:46.625144', 'plate-s-dlinnym-rukavom-411');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (7, 'Платье длинное с разрезом', 'Сукня   А-силуету 


??Модель 1003
?? Ціна 430грн
?? Розміри 1(40-42) 2(44-46) ??Колір чорний 
??Тканина дайвінг (хороша розтяжність) 
??Спинка йде на блискавці

?? 
Шикарні сукні з дайвінгу, для найстрункіших красунь Практична зручна сукня в якій, ти будеш чарівна будь-якого вечора??

??Довжина 114см 
??Довжина рукава 60см
___Заміри
1(40-42) ОГ 80-86 ОБ 88-94

2(44-46) ОГ 88-94 ОБ 96-102


??Питання/відповідь @Natadeva_7km', '1003', 430, 'UAH', '2023-10-29 13:18:40.892102', 1, 1, '2023-10-30 19:12:46.625144', 'plate-dlinnoe-s-razrezom-1003');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (8, 'Костюм черный с длинным рукавом', '[ Альбом ]
??NEW collection??

Мод. 1018
??Костюм??

?? Ціна 390грн 
??Розмір 
   універсал 42-46 
??Тканина рубчик 
?? Колір чорний ?? 



Топ з довгими рукавами та еластичні лосини з високою посадкою на резинці = якісний, практичний і водночас стильний та функціональний комплект!

??Відправляємо на клієнта ?? @Natadeva_7km', '1018', 390, 'UAH', '2023-10-29 13:48:49.466215', 3, 1, '2023-10-30 19:12:46.625144', 'kostjum-chernyj-s-dlinnym-rukavom-1018');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (9, 'Костюм легкий с коротким рукавом', 'Цена 200грн ??



? ?????? ???????????????????? ?

?? Сукня ?? 

?? Мод. 1013
?? Розмір 
   універсал 42-46
??Тканина рубчик                 Мустанг(добре тягнеться та приємна до тiла) 
?? Кольори:чорний ??, беж та меланж 


??Довжина 110см 

Стильна, облягаюча, базова сукня з зав''язками, що  чудово впишеться в літній гардероб!


??Відправляємо на клієнта @Natadeva_7km', '1013', 200, 'UAH', '2023-10-29 19:22:35.583753', 3, 1, '2023-10-30 19:12:46.625144', 'kostjum-legkij-s-korotkim-rukavom-1013');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (10, 'Платье солнце клеш', '[ Альбом ]
??Знову в наявності) 

Чарівна і чудова сукня, в якій ви не залишитеся поза увагою зі спідницею сонце ? клеш
?? Модель 435 
Ціна опт  330грн

?? Розміри: 42-44 та 46-48 ???? 
?? Тканина дайвінг ?? добре тягнеться та приемна до тiла

??Кольори
бутилка, темно-синій,   червоний 
?? Замiри 42-44 
Грудь 82-88 
Стегна 90-96 
Довжина 85 
Рукав 60 

?? Замiри 46-48 
Грудь 90-96 
Стегна 98-104
Довжина 87
Рукав 60 

?? Контакти @Natadeva_7km', '435', 330, 'UAH', '2023-10-29 19:32:57.510554', 1, 1, '2023-10-30 19:12:46.625144', 'plate-solntse-klesh-435');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (11, 'Платье рубчик с разрезом', '?????? ???????????????????? ?

?? Мод. 1026

Сукня - плаття??

??Ціна 350грн 

Зручна  сукня-водолазка ідеально сідає на фігурі, підкреслює жіночність і при цьому не стискує рухів. ———————————— 

Тканина: Турецький рубчик Мустанг 
Розмір універсал 42-46 (гарно тягнеться) 
Колір ?? мокко


??Заміри
Довжина 102см
Грудь 82-90
Стегна 90-98', '1026', 350, 'UAH', '2023-10-29 19:41:42.941907', 1, 1, '2023-10-30 19:12:46.625144', 'plate-rubchik-s-razrezom-1026');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (12, 'Платье квадратный вырез', '[ Альбом ]
 ??New collection ??

??Сукня 
??Мод. 1030
??Ціна 300грн 
??Розмір 40-42 та 44-46 
??Тканина :креп дайвінг 
??Колір чорний ?? 
??Довжина 85см 

 Приголомшливе ?? міні плаття, яке має бути у будь-якої красивої дівчини?? Неповторний образ та вишуканий смак ??

?? Питання /відповідь
@Natadeva_7km', '1030', 300, 'UAH', '2023-10-30 08:35:12.327477', 1, 1, '2023-10-30 19:12:46.625144', 'plate-kvadratnyj-vyrez-1030');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (13, 'Платье квадратный разрез длинное', '[ Альбом ]
??NEW collection ??
Ця елегантна сукня міді підкорить ваше серце з першого погляду ??

??Мод. 1029
??Сукня 
??Тканина креп-дайвінг 
??Розмір 40-42 та 44-46 
??Колір чорний ?? 
??Ціна 350грн
 
?? Довжина сукні 105см 

 Сексуально-облягаюча сукня з довгими рукавами і вирізом на нозі в актуальному чорному кольорі!Стане вашим фаворітом ??


Питання /відповідь
?? @Natadeva_7km', '1029', 350, 'UAH', '2023-10-30 08:43:01.096095', 1, 1, '2023-10-30 19:12:46.625144', 'plate-kvadratnyj-razrez-dlinnoe-1029');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (14, 'Костюм меланжевый трехнитка', '[ Альбом ]
? New ???????????????????? ?
Нове надходження жіночих двійок для модних образів навіть у найнегідніші будні!
————————————————
?? Костюм 
??Мод. 1028
Тканина: 3хнитка на флісі
Розміри: One Size (42/46)
Ціна 550грн
Колір Меланж (сірий)

?? Питання /відповідь
@Natadeva_7km', '1028', 550, 'UAH', '2023-10-30 08:48:56.454002', 3, 1, '2023-10-30 19:12:46.625144', 'kostjum-melanzhevyj-trehnitka-1028');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (15, 'Костюм велюровый', 'New collection ??

Мод. 1021

??Ціна 550

?? Костюм 2ка 
?? Тканина велюр
?? Розмір універсал 42-46 
??Колір  малина та синій

Параметри 
Грудь 82-92 
Стегна 90-100

Вирішили порадувати вас таким стильним костюмом: хіт цього сезону - штани + zip топ з капюшоном. Зустрічай осінь яскраво ??

?? Замовлення пишіть
@Natadeva_7km', '1021', 550, 'UAH', '2023-10-30 10:11:44.212387', 3, 1, '2023-10-30 19:12:46.625144', 'kostjum-veljurovyj-1021');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (16, 'Костюм из флиса черный', '? ?????? ???????????????????? ?

Костюм??світшот та штани

?? Мод. 1024
?? Розмір універсал 
   42-46 та 48-52 
??Тканина: Двосторонній фліс
??Колір чорний 
??Ціна 550грн

Зігріваємось у холодні сезони нашими теплими, якісними костюмами-двійками – світшот та штани! ————————————————
Відправляємо на клієнта ?? @Natadeva_7km', '1024', 550, 'UAH', '2023-10-30 15:56:54.363724', 3, 1, '2023-10-30 19:12:46.625144', 'kostjum-iz-flisa-chernyj-1024');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (17, 'Костюм кофта и штаны', '[ Альбом ]
?????? ????????????????????

М.1020
Костюм (штани+кофта) 
??Ціна 450грн 
?Тканина Рубчік(добре тягнеться) 
?Колір чорний, малина
?Розмір 42-46 

Параметри 
Ог 82-90 
Стегна 90-100

Шикарний та актуальний костюм-двійка це поєднання стилю, комфорту та якості!

?? Замовлення пишіть
@Natadeva_7km', '1020', 450, 'UAH', '2023-10-30 16:53:29.540855', 3, 1, '2023-10-30 20:36:05.519263', 'kostjum-kofta-i-shtany-1020');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (18, 'Платье с змейкой мангуст', '[ Альбом ]




??NEW COLLECTION??

??Сукня
??Мод. 1023
?? Розмір універсал 42-46 
??Колір чорний, маліна та беж
??Тканина Мустанг рубчик
??Ціна 370грн 

??Довжина 85см 
??Параметри 
Ог 82-90
Ос 90-98

Облягаючий, сексуальний крій сукні з довгими рукавами доповнений змійкою в ділянці грудей та стегна??

??Відправляємо на клієнта @Natadeva_7km', '1023', 370, 'UAH', '2023-10-30 20:24:16.164545', 1, 1, '2023-10-30 20:35:59.342267', 'plate-s-zmejkoj-mangust-1023');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (19, 'Юбка черная с вырезом', '[ Альбом ]
? ?????? ???????????????????? ? Шикарна спідниця міді з бічним вирізом підкорить усіх модниць своїм якісним виконанням і дизайном! ———————————————— 


??Спідниця??

?? Мод. 1017
??Ціна 200грн 
??Тканина: мікро дайвінг (добре тягнеться) 
??Розмір: 42-46 (єдиний)
??Колір ?? чорний 

????????????????
        Заміри
Довжина 95см
Стегна 90-100

?? Відправляємо на клієнта 
@Natadeva_7km', '1017', 200, 'UAH', '2023-10-30 20:28:49.405229', 4, 1, '2023-10-30 20:35:53.013282', 'jubka-chernaja-s-vyrezom-1017');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (20, 'Костюм лосины - кофта мустанг', '??Костюм??
??Модель 448
??Ціна 460грн
??Тканина: Мустанг Рубчик(Туреччина) 
??Кольори : молоко, синій та меланж ??Розміри:
42-44 та 46-48

??Сьогодні в тренді легкість і практичність, зручність та універсальність. Неймовірне почуття комфорту принесе вам стильний костюм ??

Відправляємо на клієнта @Natadeva_7km', '448', 460, 'UAH', '2023-10-30 20:51:52.055220', 3, 1, '2023-10-30 20:52:11.031783', 'kostjum-losiny-kofta-mustang-448');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (21, 'Блузка широкий рукав', '??Блузка??

??Мод 1014
??Ціна 320грн
??Розмір 42-44 44-46 
??Тканина:літня костюмка 
??Колір:чорний ??, червоний та беж 

?? Заміри 

42-44 Ог 82-86
44-46 ог 86-90

 Топові кофточки нададуть повсякденному образу родзинки. Приємні до тіла та ніжні.Спинка йде на блискавці ??

Відправляємо на клієнта
@Natadeva_7km', '1014', 320, 'UAH', '2023-10-31 17:33:46.355109', 5, 1, '2023-10-31 17:33:54.969924', 'bluzka-shirokij-rukav-1014');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (22, 'Рубашка женская', '??NEW NEW NEW?? 

??Додали новий
    Колір??

??Базова сорочка в стилі оверсайз ??

??Мод. 465 
??Ціна 320грн 
??Розмір:42-50 
??Ідеальна посадка та базова річ у вашому гардеробі ?? 
??Тканина:лайт 
?? Колір :блакитний та білий 
??Довжина:73см 
??Груди по сорочці 118см

?? Відправляємо на клієнта @Natadeva_7km', '465', 320, 'UAH', '2023-11-02 19:23:49.657980', 5, 1, '2023-11-02 19:23:49.657980', 'rubashka-zhenskaja-465');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (23, 'Платье с вырезом', '? ?????? ???????????????????? ?

??Сукня ??

м. 1019
??Ціна 350грн
Розмір універсал 42-46
Тканина Рубчік
Колір чорний та шоколад 
?? Довжина 110
?? Ог 82-90
?? Ос 90-98

Ніжна, приємна до тіла повсякденна сукня чудово підійде для дівчат, які бажають підкреслити свою жіночність і не втратити почуття комфорту!


?? Відправляємо на клієнта
@Natadeva_7km', '1019', 350, 'UAH', '2023-11-03 19:14:41.844165', 1, 1, '2023-11-03 19:14:41.844165', 'plate-s-vyrezom-1019');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (24, 'Топ с длинным рукавом', '? ???????????????????? ? Встигайте за нашими новими топами з довгими рукавами для повсякденної основи! ———————————————— 

?? Мод. 1027
??Тканина: Мікро-дайвінг
?? Розмір: 42-46 (єдиний) 
??Ціна: 220грн
??Колір ?? чорний


?? Відповідь/питання
@Natadeva_7km', '1027', 220, 'UAH', '2023-11-03 19:16:33.925686', 5, 1, '2023-11-03 19:16:33.925686', 'top-s-dlinnym-rukavom-1027');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (25, 'Платье квадратный вырез', 'Сукня ?? довжина максі А-силуету 

??Модель 1002 
?? Ціна 430грн
?? Розміри 1(40-42) 2(44-46)
??Колір чорний 
??Тканина дайвінг (хороша розтяжність) 
??Спинка йде на блискавці



??Довжина 140см 
??Довжина рукава 62см
___Заміри
1(40-42) ОГ 80-86 ОБ 88-94

2(44-46) ОГ 88-94 ОБ 96-102

??Відправляємо на клієнта 
@Natadeva_7km

Топова сукня зі спокусливим вирізом, зроблять ваш образ чарівним ?? Зручна і дуже приємна посадка ?? Виглядає просто ідеально ??', '1002', 430, 'UAH', '2023-11-03 19:21:55.105947', 1, 1, '2023-11-05 16:36:52.777492', 'plate-kvadratnyj-vyrez-1002');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (26, 'Платье малина миди с вырезом', '??  ?? ????????  ?????????????????????? ?? ??
   

??Сукня ??
??Мод. 1031

?? Розмір універсал 42-46
??Тканина рубчик Мустанг ??
??Колір :малина
??Довжина 125см

?? Ціна 390грн

Параметри
Ог 82-90
Ос 90-98


??Питання
@Natadeva_7km', '1031', 390, 'UAH', '2023-11-07 18:40:36.832784', 1, 1, '2023-11-07 18:40:40.035595', 'plate-malina-midi-s-vyrezom-1031');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (27, 'Платье с вырезом из дайвинга миди', '?? Яка Новинка ??????
     ??Сукня??
??модель 447
?? Ціна 400грн 
??Розміри: 42-44 46-48 Тканина дайвінг
(добре тягнеться та приемна до тiла) 
Колір ?? гірчиця,бутылка і червоний ??


?? Замiри 42-44 
Грудь 82-88  
Стегна 90-96
Довжина 108
Рукав 64

?? Замiри 46-48 
Грудь 90-96
Стегна 98-104
Довжина 108
Рукав 64 

Чарівна і дуже елегантна сукня ?? Обманка у вигляді корсету??
Шикарна посадка сідає просто ідеально ?? Кохання з першого погляду! Яскравий соковитий образ для наших модниць ??

Відправляємо на клієнта @Natadeva_7km', '447', 400, 'UAH', '2023-11-11 10:01:52.297400', 1, 1, '2023-11-16 08:45:02.945865', 'plate-s-vyrezom-iz-dajvinga-midi-447');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (28, 'Штаны барашек', '? ?????????????? ???????????????????? ?
Найкращі ходові джоггери ?? Якісні, м''які, затишні та практичні ??
——————————————
?? Мод. 1032

?? Тканина: полар фліс
?? Розміри: 42-46 та 48-52
?? Ціна: 250 грн

??Кольори: чорний, хакі і беж


??Питання \відповідь
@Natadeva_7km', '1032', 250, 'UAH', '2023-11-16 19:23:47.435234', 6, 1, '2023-11-16 19:23:47.435234', 'shtany-barashek-1032');
INSERT INTO catalog_product (id, title, description, sku, price, currency, created_at, category_id, is_active, updated_at, slug) VALUES (29, 'Платье прямое теплое', '? ?????? ???????????????????? ?

?? Сукня

?? Мод. 1025
?? Розмір 42-44 і 46-48 
??Тканина: Двосторонній фліс(тепла та приємна к тілу) 
??Колір чорний 
??Ціна 320грн

Довжина сукні 90см

Зігріваємось у холодні сезони нашими теплами сукнями————————————————
Відправляємо на клієнта ?? @Natadeva_7km', '1025', 320, 'UAH', '2023-11-16 19:27:56.316887', 1, 1, '2023-11-16 19:27:56.316887', 'plate-prjamoe-teploe-1025');

-- Таблица: catalog_product_colors
CREATE TABLE IF NOT EXISTS "catalog_product_colors" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "product_id" bigint NOT NULL REFERENCES "catalog_product" ("id") DEFERRABLE INITIALLY DEFERRED, "color_id" bigint NOT NULL REFERENCES "catalog_color" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (10, 3, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (11, 4, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (12, 5, 1);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (13, 6, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (14, 7, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (15, 8, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (16, 9, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (17, 9, 4);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (18, 9, 5);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (19, 10, 2);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (20, 10, 6);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (21, 10, 7);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (22, 11, 8);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (23, 12, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (24, 13, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (25, 14, 5);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (26, 15, 9);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (27, 15, 10);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (28, 16, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (29, 17, 9);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (30, 17, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (31, 18, 9);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (32, 18, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (33, 18, 4);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (34, 19, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (35, 20, 10);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (36, 20, 11);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (37, 20, 5);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (38, 21, 2);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (39, 21, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (40, 21, 4);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (41, 22, 1);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (42, 22, 12);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (43, 23, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (44, 23, 13);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (45, 24, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (46, 25, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (47, 26, 5);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (48, 27, 2);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (49, 27, 6);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (50, 27, 14);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (51, 28, 3);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (52, 28, 4);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (53, 28, 15);
INSERT INTO catalog_product_colors (id, product_id, color_id) VALUES (54, 29, 3);

-- Таблица: catalog_product_sizes
CREATE TABLE IF NOT EXISTS "catalog_product_sizes" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "product_id" bigint NOT NULL REFERENCES "catalog_product" ("id") DEFERRABLE INITIALLY DEFERRED, "size_id" bigint NOT NULL REFERENCES "catalog_size" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (7, 3, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (8, 4, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (9, 4, 4);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (10, 5, 5);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (11, 5, 6);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (12, 6, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (13, 6, 4);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (15, 7, 7);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (16, 7, 8);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (17, 8, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (18, 9, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (19, 10, 5);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (20, 10, 6);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (21, 11, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (22, 12, 8);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (23, 12, 7);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (24, 13, 8);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (25, 13, 7);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (26, 14, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (27, 15, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (28, 16, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (29, 16, 4);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (30, 17, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (31, 18, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (32, 19, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (33, 20, 5);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (34, 20, 6);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (35, 21, 8);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (36, 21, 5);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (37, 22, 9);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (38, 23, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (39, 24, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (40, 25, 8);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (41, 25, 7);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (42, 26, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (43, 27, 5);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (44, 27, 6);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (45, 28, 3);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (46, 28, 4);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (47, 29, 5);
INSERT INTO catalog_product_sizes (id, product_id, size_id) VALUES (48, 29, 6);

-- Таблица: catalog_productmodification
CREATE TABLE IF NOT EXISTS "catalog_productmodification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "stock" integer unsigned NOT NULL CHECK ("stock" >= 0), "price" integer NOT NULL, "currency" varchar(3) NOT NULL, "custom_sku" varchar(30) NOT NULL, "color_id" bigint NOT NULL REFERENCES "catalog_color" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "catalog_product" ("id") DEFERRABLE INITIALLY DEFERRED, "size_id" bigint NOT NULL REFERENCES "catalog_size" ("id") DEFERRABLE INITIALLY DEFERRED, "slug" varchar(200) NOT NULL, "created_at" datetime NOT NULL, "is_active" bool NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (30, 4, 250, 'UAH', '1005-черный-42-46', 3, 3, 3, 'bodi-chernyi-1005-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-11-05 11:47:28.264112');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (31, 0, 250, 'UAH', '1004-черный-42-46', 3, 4, 3, 'bodi-chernyi-1004-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-11-06 11:11:14.055420');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (32, 0, 250, 'UAH', '1004-черный-48-52', 3, 4, 4, 'bodi-chernyi-1004-chernyi-48-52-chernyi-48-52', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (33, 0, 280, 'UAH', '1022-белый-42-44', 1, 5, 5, 'plate-beloe-1022-belyi-42-44-belyi-42-44', '2023-10-31 17:28:54.506445', 1, '2023-11-15 20:23:51.836332');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (34, 0, 280, 'UAH', '1022-белый-46-48', 1, 5, 6, 'plate-beloe-1022-belyi-46-48-belyi-46-48', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (35, 1, 400, 'UAH', '411-черный-42-46', 3, 6, 3, 'plate-s-dlinnym-rukavom-411-chernyi-42-46-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-11-12 17:15:38.786815');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (36, 0, 400, 'UAH', '411-черный-48-52', 3, 6, 4, 'plate-s-dlinnym-rukavom-411-chernyi-48-52-chernyi-48-52', '2023-10-31 17:28:54.506445', 1, '2023-11-12 17:14:13.431933');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (39, 0, 430, 'UAH', '1003-черный-40-42', 3, 7, 7, 'plate-dlinnoe-s-razrezom-1003-chernyi-40-42-chernyi-40-42', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (40, 0, 430, 'UAH', '1003-черный-44-46', 3, 7, 8, 'plate-dlinnoe-s-razrezom-1003-chernyi-44-46-chernyi-44-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (41, 0, 390, 'UAH', '1018-черный-42-46', 3, 8, 3, 'kostium-chernyi-s-dlinnym-rukavom-1018-chernyi-42-46-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (42, 0, 200, 'UAH', '1013-черный-42-46', 3, 9, 3, 'kostium-legkii-s-korotkim-rukavom-1013-chernyi-42-46-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-11-16 08:55:38.094401');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (43, 0, 200, 'UAH', '1013-беж-42-46', 4, 9, 3, 'kostium-legkii-s-korotkim-rukavom-1013-bezh-42-46-bezh-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (44, 0, 200, 'UAH', '1013-меланж-42-46', 5, 9, 3, 'kostium-legkii-s-korotkim-rukavom-1013-melanzh-42-46-melanzh-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (45, 3, 330, 'UAH', '435-красный-42-44', 2, 10, 5, 'plate-solntse-klesh-435-krasnyi-42-44-krasnyi-42-44', '2023-10-31 17:28:54.506445', 1, '2023-11-16 19:18:02.381971');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (46, 0, 330, 'UAH', '435-красный-46-48', 2, 10, 6, 'plate-solntse-klesh-435-krasnyi-46-48-krasnyi-46-48', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (47, 5, 330, 'UAH', '435-бутылка-42-44', 6, 10, 5, 'plate-solntse-klesh-435-butylka-42-44-butylka-42-44', '2023-10-31 17:28:54.506445', 1, '2023-11-15 19:45:59.874237');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (48, 0, 330, 'UAH', '435-бутылка-46-48', 6, 10, 6, 'plate-solntse-klesh-435-butylka-46-48-butylka-46-48', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (49, 0, 330, 'UAH', '435-темно-синий-42-44', 7, 10, 5, 'plate-solntse-klesh-435-temno-sinii-42-44-temno-sinii-42-44', '2023-10-31 17:28:54.506445', 1, '2023-11-16 06:53:24.527315');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (50, 0, 330, 'UAH', '435-темно-синий-46-48', 7, 10, 6, 'plate-solntse-klesh-435-temno-sinii-46-48-temno-sinii-46-48', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (51, 0, 350, 'UAH', '1026-мокко-42-46', 8, 11, 3, 'plate-rubchik-s-razrezom-1026-mokko-42-46-mokko-42-46', '2023-10-31 17:28:54.506445', 1, '2023-11-15 19:55:26.750239');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (52, 0, 300, 'UAH', '1030-черный-40-42', 3, 12, 7, 'plate-kvadratnyi-vyrez-1030-chernyi-40-42-chernyi-40-42', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (53, 0, 300, 'UAH', '1030-черный-44-46', 3, 12, 8, 'plate-kvadratnyi-vyrez-1030-chernyi-44-46-chernyi-44-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (54, 0, 350, 'UAH', '1029-черный-40-42', 3, 13, 7, 'plate-kvadratnyi-razrez-dlinnoe-1029-chernyi-40-42-chernyi-40-42', '2023-10-31 17:28:54.506445', 1, '2023-11-15 19:58:18.567799');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (55, 0, 350, 'UAH', '1029-черный-44-46', 3, 13, 8, 'plate-kvadratnyi-razrez-dlinnoe-1029-chernyi-44-46-chernyi-44-46', '2023-10-31 17:28:54.506445', 1, '2023-11-15 19:58:14.362518');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (56, 0, 550, 'UAH', '1028-меланж-42-46', 5, 14, 3, 'kostium-melanzhevyi-trekhnitka-1028-melanzh-42-46-melanzh-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (57, 0, 550, 'UAH', '1021-малина-42-46', 9, 15, 3, 'kostium-veliurovyi-1021-malina-42-46-malina-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (58, 0, 550, 'UAH', '1021-синий-42-46', 10, 15, 3, 'kostium-veliurovyi-1021-sinii-42-46-sinii-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (59, 0, 550, 'UAH', '1024-черный-42-46', 3, 16, 3, 'kostium-iz-flisa-chernyi-1024-chernyi-42-46-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (60, 0, 550, 'UAH', '1024-черный-48-52', 3, 16, 4, 'kostium-iz-flisa-chernyi-1024-chernyi-48-52-chernyi-48-52', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (61, 0, 450, 'UAH', '1020-малина-42-46', 9, 17, 3, 'kostium-kofta-i-shtany-1020-malina-42-46-malina-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (62, 2, 450, 'UAH', '1020-черный-42-46', 3, 17, 3, 'kostium-kofta-i-shtany-1020-chernyi-42-46-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-11-16 08:49:05.357357');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (63, 0, 370, 'UAH', '1023-беж-42-46', 4, 18, 3, 'plate-s-zmeikoi-mangust-1023-bezh-42-46-bezh-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (64, 0, 370, 'UAH', '1023-малина-42-46', 9, 18, 3, 'plate-s-zmeikoi-mangust-1023-malina-42-46-malina-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (65, 0, 370, 'UAH', '1023-черный-42-46', 3, 18, 3, 'plate-s-zmeikoi-mangust-1023-chernyi-42-46-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (66, 0, 200, 'UAH', '1017-черный-42-46', 3, 19, 3, 'iubka-chernaia-s-vyrezom-1017-chernyi-42-46', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (67, 0, 460, 'UAH', '448-меланж-42-44', 5, 20, 5, 'kostium-losiny-kofta-mustang-448-melanzh-42-44-melanzh-42-44', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (68, 0, 460, 'UAH', '448-меланж-46-48', 5, 20, 6, 'kostium-losiny-kofta-mustang-448-melanzh-46-48-melanzh-46-48', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (69, 0, 460, 'UAH', '448-молоко-42-44', 11, 20, 5, 'kostium-losiny-kofta-mustang-448-moloko-42-44-moloko-42-44', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (70, 0, 460, 'UAH', '448-молоко-46-48', 11, 20, 6, 'kostium-losiny-kofta-mustang-448-moloko-46-48-moloko-46-48', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (71, 0, 460, 'UAH', '448-синий-42-44', 10, 20, 5, 'kostium-losiny-kofta-mustang-448-sinii-42-44-sinii-42-44', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (72, 0, 460, 'UAH', '448-синий-46-48', 10, 20, 6, 'kostium-losiny-kofta-mustang-448-sinii-46-48-sinii-46-48', '2023-10-31 17:28:54.506445', 1, '2023-10-31 17:28:54.522949');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (73, 0, 320, 'UAH', '1014-беж-42-44', 4, 21, 5, 'bluzka-shirokii-rukav-1014-bezh-42-44-bezh-42-44', '2023-10-31 17:33:46.361658', 1, '2023-10-31 17:33:46.361658');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (74, 3, 320, 'UAH', '1014-беж-44-46', 4, 21, 8, 'bluzka-shirokii-rukav-1014-bezh-44-46-bezh-44-46', '2023-10-31 17:33:46.362658', 1, '2023-11-16 08:49:05.356356');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (75, 0, 320, 'UAH', '1014-красный-42-44', 2, 21, 5, 'bluzka-shirokii-rukav-1014-krasnyi-42-44-krasnyi-42-44', '2023-10-31 17:33:46.362658', 1, '2023-10-31 17:33:46.362658');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (76, 0, 320, 'UAH', '1014-красный-44-46', 2, 21, 8, 'bluzka-shirokii-rukav-1014-krasnyi-44-46-krasnyi-44-46', '2023-10-31 17:33:46.362658', 1, '2023-10-31 17:35:00.932570');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (77, 0, 320, 'UAH', '1014-черный-42-44', 3, 21, 5, 'bluzka-shirokii-rukav-1014-chernyi-42-44-chernyi-42-44', '2023-10-31 17:33:46.362658', 1, '2023-10-31 17:33:46.362658');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (78, 2, 320, 'UAH', '1014-черный-44-46', 3, 21, 8, 'bluzka-shirokii-rukav-1014-chernyi-44-46-chernyi-44-46', '2023-10-31 17:33:46.362658', 1, '2023-11-16 08:44:31.332165');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (79, 0, 320, 'UAH', '465-белый-42-50', 1, 22, 9, 'rubashka-zhenskaia-465-belyi-42-50-belyi-42-50', '2023-11-02 19:23:49.665051', 1, '2023-11-02 19:24:39.240427');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (80, 0, 320, 'UAH', '465-голубой-42-50', 12, 22, 9, 'rubashka-zhenskaia-465-goluboi-42-50-goluboi-42-50', '2023-11-02 19:23:49.665051', 1, '2023-11-02 19:24:24.021635');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (81, 0, 350, 'UAH', '1019-черный-42-46', 3, 23, 3, 'plate-s-vyrezom-1019-chernyi-42-46-chernyi-42-46', '2023-11-03 19:14:41.852677', 1, '2023-11-03 19:15:22.810150');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (82, 0, 350, 'UAH', '1019-шоколад-42-46', 13, 23, 3, 'plate-s-vyrezom-1019-shokolad-42-46-shokolad-42-46', '2023-11-03 19:14:41.853678', 1, '2023-11-03 19:15:14.339180');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (83, 0, 220, 'UAH', '1027-черный-42-46', 3, 24, 3, 'top-s-dlinnym-rukavom-1027-chernyi-42-46-chernyi-42-46', '2023-11-03 19:16:33.933194', 1, '2023-11-03 19:16:59.377335');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (84, 4, 430, 'UAH', '1002-черный-40-42', 3, 25, 7, 'plate-kvadratnyi-vyrez-1002-chernyi-40-42-chernyi-40-42', '2023-11-03 19:21:55.111457', 1, '2023-11-15 19:57:00.904277');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (85, 12, 430, 'UAH', '1002-черный-44-46', 3, 25, 8, 'plate-kvadratnyi-vyrez-1002-chernyi-44-46-chernyi-44-46', '2023-11-03 19:21:55.112458', 1, '2023-11-16 08:44:31.331158');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (86, 0, 390, 'UAH', '1031-меланж-42-46', 5, 26, 3, 'plate-malina-midi-s-vyrezom-1031-melanzh-42-46-melanzh-42-46', '2023-11-07 18:40:36.840288', 1, '2023-11-07 18:41:27.457519');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (87, 9, 400, 'UAH', '447-бутылка-42-44', 6, 27, 5, 'plate-s-vyrezom-iz-daivinga-midi-447-butylka-42-44-butylka-42-44', '2023-11-11 10:01:52.304415', 1, '2023-11-12 17:12:13.901622');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (88, 8, 400, 'UAH', '447-бутылка-46-48', 6, 27, 6, 'plate-s-vyrezom-iz-daivinga-midi-447-butylka-46-48-butylka-46-48', '2023-11-11 10:01:52.305415', 1, '2023-11-14 08:14:35.975955');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (89, 3, 400, 'UAH', '447-горчица-42-44', 14, 27, 5, 'plate-s-vyrezom-iz-daivinga-midi-447-gorchitsa-42-44-gorchitsa-42-44', '2023-11-11 10:01:52.305415', 1, '2023-11-16 18:33:42.623930');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (90, 13, 400, 'UAH', '447-горчица-46-48', 14, 27, 6, 'plate-s-vyrezom-iz-daivinga-midi-447-gorchitsa-46-48-gorchitsa-46-48', '2023-11-11 10:01:52.305415', 1, '2023-11-12 17:12:13.902623');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (91, 0, 400, 'UAH', '447-красный-42-44', 2, 27, 5, 'plate-s-vyrezom-iz-daivinga-midi-447-krasnyi-42-44-krasnyi-42-44', '2023-11-11 10:01:52.306416', 1, '2023-11-16 08:44:55.187700');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (92, 1, 400, 'UAH', '447-красный-46-48', 2, 27, 6, 'plate-s-vyrezom-iz-daivinga-midi-447-krasnyi-46-48-krasnyi-46-48', '2023-11-11 10:01:52.306416', 1, '2023-11-16 18:34:10.479048');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (93, 0, 250, 'UAH', '1032-беж-42-46', 4, 28, 3, 'shtany-barashek-1032-bezh-42-46-bezh-42-46', '2023-11-16 19:23:47.441238', 1, '2023-11-16 19:23:47.441238');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (94, 0, 250, 'UAH', '1032-беж-48-52', 4, 28, 4, 'shtany-barashek-1032-bezh-48-52-bezh-48-52', '2023-11-16 19:23:47.442238', 1, '2023-11-16 19:24:55.547969');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (95, 0, 250, 'UAH', '1032-хаки-42-46', 15, 28, 3, 'shtany-barashek-1032-khaki-42-46-khaki-42-46', '2023-11-16 19:23:47.442238', 1, '2023-11-16 19:23:47.442238');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (96, 0, 250, 'UAH', '1032-хаки-48-52', 15, 28, 4, 'shtany-barashek-1032-khaki-48-52-khaki-48-52', '2023-11-16 19:23:47.442238', 1, '2023-11-16 19:24:49.080357');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (97, 0, 250, 'UAH', '1032-черный-42-46', 3, 28, 3, 'shtany-barashek-1032-chernyi-42-46-chernyi-42-46', '2023-11-16 19:23:47.443238', 1, '2023-11-16 19:23:47.443238');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (98, 0, 250, 'UAH', '1032-черный-48-52', 3, 28, 4, 'shtany-barashek-1032-chernyi-48-52-chernyi-48-52', '2023-11-16 19:23:47.443238', 1, '2023-11-16 19:24:29.213626');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (99, 0, 320, 'UAH', '1025-черный-42-44', 3, 29, 5, 'plate-priamoe-teploe-1025-chernyi-42-44-chernyi-42-44', '2023-11-16 19:27:56.322888', 1, '2023-11-16 19:27:56.322888');
INSERT INTO catalog_productmodification (id, stock, price, currency, custom_sku, color_id, product_id, size_id, slug, created_at, is_active, updated_at) VALUES (100, 0, 320, 'UAH', '1025-черный-46-48', 3, 29, 6, 'plate-priamoe-teploe-1025-chernyi-46-48-chernyi-46-48', '2023-11-16 19:27:56.323888', 1, '2023-11-16 19:28:11.150450');

-- Таблица: catalog_return
CREATE TABLE IF NOT EXISTS "catalog_return" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "comment" text NOT NULL, "source" varchar(20) NOT NULL, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "telegram_user_id" bigint NULL REFERENCES "catalog_telegramuser" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_return (id, created_at, comment, source, user_id, telegram_user_id) VALUES (11, '2023-11-12 17:15:38.754991', '', 'telegram', NULL, NULL);
INSERT INTO catalog_return (id, created_at, comment, source, user_id, telegram_user_id) VALUES (12, '2023-11-13 10:18:47.284343', '', 'telegram', NULL, NULL);
INSERT INTO catalog_return (id, created_at, comment, source, user_id, telegram_user_id) VALUES (13, '2023-11-14 08:14:35.928052', '', 'telegram', NULL, NULL);
INSERT INTO catalog_return (id, created_at, comment, source, user_id, telegram_user_id) VALUES (14, '2023-11-15 19:45:46.533775', '', 'telegram', NULL, NULL);
INSERT INTO catalog_return (id, created_at, comment, source, user_id, telegram_user_id) VALUES (15, '2023-11-16 06:53:35.936463', '', 'telegram', NULL, NULL);
INSERT INTO catalog_return (id, created_at, comment, source, user_id, telegram_user_id) VALUES (16, '2023-11-16 08:48:56', '', 'site', NULL, NULL);

-- Таблица: catalog_returnitem
CREATE TABLE IF NOT EXISTS "catalog_returnitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "product_modification_id" bigint NOT NULL REFERENCES "catalog_productmodification" ("id") DEFERRABLE INITIALLY DEFERRED, "return_sale_id" bigint NOT NULL REFERENCES "catalog_return" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_returnitem (id, quantity, product_modification_id, return_sale_id) VALUES (11, 1, 35, 11);
INSERT INTO catalog_returnitem (id, quantity, product_modification_id, return_sale_id) VALUES (12, 1, 49, 12);
INSERT INTO catalog_returnitem (id, quantity, product_modification_id, return_sale_id) VALUES (13, 1, 88, 13);
INSERT INTO catalog_returnitem (id, quantity, product_modification_id, return_sale_id) VALUES (14, 1, 33, 14);
INSERT INTO catalog_returnitem (id, quantity, product_modification_id, return_sale_id) VALUES (15, 1, 42, 15);
INSERT INTO catalog_returnitem (id, quantity, product_modification_id, return_sale_id) VALUES (16, 3, 74, 16);
INSERT INTO catalog_returnitem (id, quantity, product_modification_id, return_sale_id) VALUES (17, 2, 62, 16);

-- Таблица: catalog_sale
CREATE TABLE IF NOT EXISTS "catalog_sale" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "comment" text NOT NULL, "payment_method" varchar(20) NOT NULL, "status" varchar(20) NOT NULL, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "source" varchar(20) NOT NULL, "telegram_user_id" bigint NULL REFERENCES "catalog_telegramuser" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (195, '2023-11-12 17:15:19.058753', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (196, '2023-11-12 17:15:33.290508', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (197, '2023-11-12 19:22:03.991710', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (198, '2023-11-13 10:20:41.020960', '', 'non_cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (199, '2023-11-13 10:30:53.776373', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (200, '2023-11-13 17:28:52.767191', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (201, '2023-11-13 20:00:59.334164', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (202, '2023-11-15 19:45:59.841964', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (203, '2023-11-15 19:59:34', '', 'cash', 'completed', NULL, 'site', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (204, '2023-11-15 20:23:51.802986', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (205, '2023-11-16 06:53:24.502273', '', 'non_cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (206, '2023-11-16 06:56:25.888028', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (207, '2023-11-16 07:01:31.633777', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (208, '2023-11-16 07:03:46.544917', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (209, '2023-11-16 07:05:03.633876', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (210, '2023-11-16 07:06:46.151154', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (211, '2023-11-16 07:08:21.791679', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (212, '2023-11-16 07:09:33.869941', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (213, '2023-11-16 07:19:34.287671', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (214, '2023-11-16 08:55:38.061833', '', 'cash', 'completed', NULL, 'telegram', NULL);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (215, '2023-11-16 17:08:08.396428', '', 'cash', 'completed', NULL, 'telegram', 6);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (216, '2023-11-16 18:33:42.590731', '', 'cash', 'completed', NULL, 'telegram', 6);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (217, '2023-11-16 18:34:10.447271', '', 'cash', 'completed', NULL, 'telegram', 6);
INSERT INTO catalog_sale (id, created_at, comment, payment_method, status, user_id, source, telegram_user_id) VALUES (218, '2023-11-16 19:18:02.350292', '', 'cash', 'completed', NULL, 'telegram', 6);

-- Таблица: catalog_saleitem
CREATE TABLE IF NOT EXISTS "catalog_saleitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "product_modification_id" bigint NOT NULL REFERENCES "catalog_productmodification" ("id") DEFERRABLE INITIALLY DEFERRED, "sale_id" bigint NOT NULL REFERENCES "catalog_sale" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (228, 1, 45, 195);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (229, 1, 49, 196);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (230, 1, 45, 197);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (231, 2, 45, 198);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (232, 2, 45, 199);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (233, 2, 45, 200);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (234, 1, 47, 201);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (235, 2, 47, 202);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (236, 1, 91, 203);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (237, 1, 33, 204);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (238, 1, 49, 205);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (239, 1, 45, 213);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (240, 1, 42, 214);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (241, 1, 89, 215);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (242, 2, 89, 216);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (243, 2, 92, 217);
INSERT INTO catalog_saleitem (id, quantity, product_modification_id, sale_id) VALUES (244, 2, 45, 218);

-- Таблица: catalog_size
CREATE TABLE IF NOT EXISTS "catalog_size" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(10) NOT NULL UNIQUE);
INSERT INTO catalog_size (id, name) VALUES (3, '42-46');
INSERT INTO catalog_size (id, name) VALUES (4, '48-52');
INSERT INTO catalog_size (id, name) VALUES (5, '42-44');
INSERT INTO catalog_size (id, name) VALUES (6, '46-48');
INSERT INTO catalog_size (id, name) VALUES (7, '40-42');
INSERT INTO catalog_size (id, name) VALUES (8, '44-46');
INSERT INTO catalog_size (id, name) VALUES (9, '42-50');

-- Таблица: catalog_telegramuser
CREATE TABLE IF NOT EXISTS "catalog_telegramuser" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL UNIQUE, "user_name" varchar(255) NULL, "first_name" varchar(255) NOT NULL, "last_name" varchar(255) NULL, "is_bot" bool NOT NULL, "created_at" datetime NOT NULL, "role" varchar(12) NOT NULL);
INSERT INTO catalog_telegramuser (id, user_id, user_name, first_name, last_name, is_bot, created_at, role) VALUES (2, 732831833, 'Natadeva_7km', 'Ната', NULL, 0, '2023-11-11 16:06:56.668822', 'admin');
INSERT INTO catalog_telegramuser (id, user_id, user_name, first_name, last_name, is_bot, created_at, role) VALUES (6, 774411051, NULL, 'Arg??', NULL, 0, '2023-11-16 16:10:14.060575', 'admin');

-- Таблица: catalog_writeoff
CREATE TABLE IF NOT EXISTS "catalog_writeoff" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "comment" text NOT NULL, "status" varchar(20) NOT NULL, "telegram_user_id" bigint NULL REFERENCES "catalog_telegramuser" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_writeoff (id, created_at, comment, status, telegram_user_id, user_id) VALUES (2, '2023-11-16 08:29:22', '', 'completed', NULL, NULL);
INSERT INTO catalog_writeoff (id, created_at, comment, status, telegram_user_id, user_id) VALUES (3, '2023-11-16 08:44:45', '', 'completed', NULL, NULL);

-- Таблица: catalog_writeoffitem
CREATE TABLE IF NOT EXISTS "catalog_writeoffitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "product_modification_id" bigint NOT NULL REFERENCES "catalog_productmodification" ("id") DEFERRABLE INITIALLY DEFERRED, "write_off_id" bigint NOT NULL REFERENCES "catalog_writeoff" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO catalog_writeoffitem (id, quantity, product_modification_id, write_off_id) VALUES (2, 2, 91, 2);
INSERT INTO catalog_writeoffitem (id, quantity, product_modification_id, write_off_id) VALUES (3, 2, 91, 3);

-- Таблица: django_admin_log
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (1, '1', 'Платья', 1, '[{"added": {}}]', 9, 1, '2023-10-28 09:52:40.758161');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (2, '1', 'белый', 1, '[{"added": {}}]', 11, 1, '2023-10-28 09:52:51.306914');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (3, '2', 'красный', 1, '[{"added": {}}]', 11, 1, '2023-10-28 09:52:54.385714');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (4, '1', '42', 1, '[{"added": {}}]', 12, 1, '2023-10-28 09:52:58.874492');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (5, '2', '44', 1, '[{"added": {}}]', 12, 1, '2023-10-28 09:53:02.936517');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (6, '1', 'asdaads', 1, '[{"added": {}}]', 7, 1, '2023-10-28 09:53:07.210012');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (7, '1', 'Image object (1)', 1, '[{"added": {}}]', 10, 1, '2023-10-28 09:54:08.947015');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (8, '1', 'Image object (1)', 2, '[]', 10, 1, '2023-10-28 09:54:15.979773');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (9, '2', 'Image object (2)', 1, '[{"added": {}}]', 10, 1, '2023-10-28 09:58:27.437602');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (10, '3', 'Image object (3)', 1, '[{"added": {}}]', 10, 1, '2023-10-28 10:01:19.636547');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (11, '1', 'Image object (1)', 2, '[]', 10, 1, '2023-10-28 10:01:24.597299');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (12, '4', 'Image object (4)', 1, '[{"added": {}}]', 10, 1, '2023-10-28 10:09:49.209602');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (13, '5', 'Image object (5)', 1, '[{"added": {}}]', 10, 1, '2023-10-28 10:09:53.101107');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (14, '6', 'Image object (6)', 1, '[{"added": {}}]', 10, 1, '2023-10-28 10:09:56.691618');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (15, '6', 'Image object (6)', 2, '[]', 10, 1, '2023-10-28 10:17:46.409923');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (16, '5', 'Image object (5)', 2, '[]', 10, 1, '2023-10-28 10:17:48.877089');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (17, '4', 'Image object (4)', 2, '[]', 10, 1, '2023-10-28 10:17:59.292716');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (18, '7', 'Image object (7)', 1, '[{"added": {}}]', 10, 1, '2023-10-28 10:41:49.474616');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (19, '3', 'asdaads - 001-красный-42', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (8)"}}]', 8, 1, '2023-10-28 10:58:22.408243');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (20, '4', 'asdaads - 001-красный-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (9)"}}]', 8, 1, '2023-10-28 10:58:27.726287');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (21, '2', 'asdaads - 001-белый-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (10)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (11)"}}]', 8, 1, '2023-10-28 10:58:43.172114');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (22, '12', 'Image object (12)', 1, '[{"added": {}}]', 10, 1, '2023-10-28 11:39:57.228794');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (23, '4', 'asdaads - 001-красный-44', 2, '[{"changed": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (9)", "fields": ["\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435"]}}]', 8, 1, '2023-10-28 11:42:32.555565');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (24, '4', 'asdaads - 001-красный-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (13)"}}]', 8, 1, '2023-10-28 11:42:55.125432');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (25, '4', 'asdaads - 001-красный-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (14)"}}]', 8, 1, '2023-10-28 11:43:14.188793');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (26, '3', 'черный', 1, '[{"added": {}}]', 11, 1, '2023-10-28 11:49:51.013800');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (27, '1', 'asdaads', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430"]}}]', 7, 1, '2023-10-28 11:49:53.081426');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (28, '6', 'asdaads - 001-черный-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (15)"}}]', 8, 1, '2023-10-28 11:50:08.946923');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (29, '6', 'asdaads - 001-черный-44', 2, '[{"changed": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (15)", "fields": ["\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435"]}}]', 8, 1, '2023-10-28 11:50:12.551346');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (30, '6', 'asdaads - 001-черный-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (16)"}}]', 8, 1, '2023-10-28 11:50:16.447549');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (31, '6', 'asdaads - 001-черный-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (17)"}}]', 8, 1, '2023-10-28 11:50:21.791586');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (32, '6', 'asdaads - 001-черный-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (18)"}}]', 8, 1, '2023-10-28 11:50:27.624321');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (33, '1', 'asdaads - 001-белый-42', 2, '[{"changed": {"fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 8, 1, '2023-10-29 08:45:31.802173');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (34, '3', 'asdaads - 001-красный-42', 2, '[{"changed": {"fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 8, 1, '2023-10-29 08:45:42.158950');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (35, '1', 'asdaads', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430"]}}]', 7, 1, '2023-10-29 08:45:51.313580');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (36, '1', 'asdaads', 2, '[]', 7, 1, '2023-10-29 08:46:00.545249');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (37, '1', 'asdaads', 2, '[]', 7, 1, '2023-10-29 08:48:17.711182');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (38, '2', 'фывфвфы', 1, '[{"added": {}}]', 7, 1, '2023-10-29 08:48:32.785122');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (39, '2', 'фывфвфы', 2, '[]', 7, 1, '2023-10-29 08:49:56.039634');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (40, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430"]}}]', 7, 1, '2023-10-29 08:50:00.579204');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (41, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0420\u0430\u0437\u043c\u0435\u0440\u044b"]}}]', 7, 1, '2023-10-29 08:50:06.448786');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (42, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0420\u0430\u0437\u043c\u0435\u0440\u044b"]}}]', 7, 1, '2023-10-29 08:50:12.861694');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (43, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430"]}}]', 7, 1, '2023-10-29 08:50:16.551487');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (44, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430"]}}]', 7, 1, '2023-10-29 08:51:34.829149');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (45, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0420\u0430\u0437\u043c\u0435\u0440\u044b"]}}]', 7, 1, '2023-10-29 08:51:39.101112');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (46, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430", "\u0420\u0430\u0437\u043c\u0435\u0440\u044b"]}}]', 7, 1, '2023-10-29 08:51:44.564135');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (47, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430"]}}]', 7, 1, '2023-10-29 08:51:50.876349');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (48, '2', 'фывфвфы', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u0444\u044b\u0432\u0444\u0432\u0444\u044b - 222-\u0431\u0435\u043b\u044b\u0439-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u0444\u044b\u0432\u0444\u0432\u0444\u044b - 222-\u0431\u0435\u043b\u044b\u0439-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-10-29 08:52:00.778027');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (49, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430"]}}]', 7, 1, '2023-10-29 08:52:06.996876');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (50, '2', 'фывфвфы', 2, '[{"changed": {"fields": ["\u0426\u0432\u0435\u0442\u0430"]}}]', 7, 1, '2023-10-29 08:52:13.035242');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (51, '2', 'фывфвфы', 2, '[]', 7, 1, '2023-10-29 08:52:24.726477');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (52, '2', 'Боди', 1, '[{"added": {}}]', 9, 1, '2023-10-29 09:22:28.213456');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (53, '3', '42-46', 1, '[{"added": {}}]', 12, 1, '2023-10-29 09:22:55.966567');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (54, '3', 'Боди черный', 1, '[{"added": {}}]', 7, 1, '2023-10-29 09:23:07.473919');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (55, '30', 'Боди черный - 1005-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (19)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (20)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (21)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (22)"}}]', 8, 1, '2023-10-29 09:24:11.291284');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (56, '3', 'Боди черный', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u0411\u043e\u0434\u0438 \u0447\u0435\u0440\u043d\u044b\u0439 - 1005-\u0447\u0435\u0440\u043d\u044b\u0439-42-46", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-10-29 09:24:33.440090');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (57, '3', 'Боди черный', 2, '[]', 7, 1, '2023-10-29 09:24:55.804901');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (58, '30', 'Боди черный - 1005-черный-42-46', 2, '[]', 8, 1, '2023-10-29 09:25:09.636824');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (59, '2', 'фывфвфы', 3, '', 7, 1, '2023-10-29 09:52:37.897157');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (60, '1', 'asdaads', 3, '', 7, 1, '2023-10-29 09:52:37.911147');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (61, '4', '48-52', 1, '[{"added": {}}]', 12, 1, '2023-10-29 09:53:42.536339');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (62, '4', 'Боди черный1', 1, '[{"added": {}}]', 7, 1, '2023-10-29 09:58:21.931223');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (63, '4', 'Боди черный', 2, '[{"changed": {"fields": ["\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435"]}}]', 7, 1, '2023-10-29 09:58:39.619358');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (64, '4', 'Боди черный', 2, '[{"changed": {"fields": ["\u0421\u043b\u0430\u0433"]}}]', 7, 1, '2023-10-29 10:02:12.981935');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (65, '4', 'Боди черный', 2, '[]', 7, 1, '2023-10-29 10:02:19.232728');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (66, '4', 'Боди черный', 2, '[]', 7, 1, '2023-10-29 10:02:24.150863');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (67, '3', 'Боди черный', 2, '[]', 7, 1, '2023-10-29 10:02:33.112841');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (68, '3', 'Боди черный', 2, '[{"changed": {"fields": ["\u0421\u043b\u0430\u0433"]}}]', 7, 1, '2023-10-29 10:02:37.825507');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (69, '3', 'Боди черный', 2, '[]', 7, 1, '2023-10-29 10:02:43.096477');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (70, '32', 'Боди черный - 1004-черный-48-52', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (23)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (24)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (25)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (26)"}}]', 8, 1, '2023-10-29 10:04:00.888403');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (71, '31', 'Боди черный - 1004-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (27)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (28)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (29)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (30)"}}]', 8, 1, '2023-10-29 10:04:18.121444');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (72, '5', '42-44', 1, '[{"added": {}}]', 12, 1, '2023-10-29 10:09:40.730998');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (73, '6', '46-48', 1, '[{"added": {}}]', 12, 1, '2023-10-29 10:09:55.068946');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (74, '5', 'Платье белое', 1, '[{"added": {}}]', 7, 1, '2023-10-29 10:10:13.960562');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (75, '5', 'Платье белое', 2, '[]', 7, 1, '2023-10-29 10:10:18.940698');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (76, '34', 'Платье белое - 1022-белый-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (31)"}}]', 8, 1, '2023-10-29 10:16:46.871250');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (77, '34', 'Платье белое - 1022-белый-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (32)"}}]', 8, 1, '2023-10-29 10:16:54.847130');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (78, '34', 'Платье белое - 1022-белый-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (33)"}}]', 8, 1, '2023-10-29 10:17:01.293854');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (79, '34', 'Платье белое - 1022-белый-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (34)"}}]', 8, 1, '2023-10-29 10:17:12.141039');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (80, '34', 'Платье белое - 1022-белый-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (35)"}}]', 8, 1, '2023-10-29 10:17:15.791237');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (81, '34', 'Платье белое - 1022-белый-46-48', 2, '[]', 8, 1, '2023-10-29 10:17:17.659243');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (82, '34', 'Платье белое - 1022-белый-46-48', 2, '[]', 8, 1, '2023-10-29 10:20:00.115325');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (83, '34', 'Платье белое - 1022-белый-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (36)"}}]', 8, 1, '2023-10-29 10:20:29.241631');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (84, '33', 'Платье белое - 1022-белый-42-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (37)"}}]', 8, 1, '2023-10-29 10:20:47.609706');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (85, '33', 'Платье белое - 1022-белый-42-44', 2, '[]', 8, 1, '2023-10-29 10:20:53.233540');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (86, '5', 'Платье белое', 2, '[]', 7, 1, '2023-10-29 10:21:07.758634');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (87, '5', 'Платье белое', 2, '[]', 7, 1, '2023-10-29 10:21:10.035972');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (88, '33', 'Платье белое - 1022-белый-42-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (38)"}}]', 8, 1, '2023-10-29 10:21:18.344519');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (89, '33', 'Платье белое - 1022-белый-42-44', 2, '[]', 8, 1, '2023-10-29 10:21:20.387629');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (90, '6', 'Платье с длинным рукавом', 1, '[{"added": {}}]', 7, 1, '2023-10-29 10:22:37.724168');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (91, '6', 'Платье с длинным рукавом', 2, '[]', 7, 1, '2023-10-29 10:22:39.278582');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (92, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (39)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (40)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (41)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (42)"}}]', 8, 1, '2023-10-29 10:23:01.070984');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (93, '35', 'Платье с длинным рукавом - 411-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (43)"}}]', 8, 1, '2023-10-29 10:23:07.960391');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (94, '35', 'Платье с длинным рукавом - 411-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (44)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (45)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (46)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (47)"}}]', 8, 1, '2023-10-29 10:24:38.768897');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (95, '33', 'Платье белое - 1022-белый-42-44', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (48)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (49)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (50)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (51)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (52)"}}]', 8, 1, '2023-10-29 10:25:00.749942');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (96, '7', '40-42', 1, '[{"added": {}}]', 12, 1, '2023-10-29 13:18:20.633451');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (97, '8', '44-46', 1, '[{"added": {}}]', 12, 1, '2023-10-29 13:18:31.756160');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (98, '7', 'Платье длинное с разрезом', 1, '[{"added": {}}]', 7, 1, '2023-10-29 13:18:40.898108');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (99, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (53)"}}]', 8, 1, '2023-10-29 13:19:21.568838');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (100, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[]', 8, 1, '2023-10-29 13:19:50.649521');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (101, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[]', 8, 1, '2023-10-29 13:19:52.760190');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (102, '37', 'Платье длинное с разрезом - 1003-черный-40-42', 2, '[]', 8, 1, '2023-10-29 13:20:05.332535');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (103, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (54)"}}]', 8, 1, '2023-10-29 13:27:42.354229');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (104, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[]', 8, 1, '2023-10-29 13:27:44.182583');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (105, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (55)"}}]', 8, 1, '2023-10-29 13:28:46.833088');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (106, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (56)"}}]', 8, 1, '2023-10-29 13:29:15.378348');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (107, '57', 'Image object (57)', 1, '[{"added": {}}]', 10, 1, '2023-10-29 13:41:01.453840');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (108, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[]', 8, 1, '2023-10-29 13:41:11.896857');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (109, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[]', 8, 1, '2023-10-29 13:41:13.518460');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (110, '38', 'Платье длинное с разрезом - 1003-черный-44-46', 3, '', 8, 1, '2023-10-29 13:42:47.608626');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (111, '37', 'Платье длинное с разрезом - 1003-черный-40-42', 3, '', 8, 1, '2023-10-29 13:42:47.620142');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (112, '7', 'Платье длинное с разрезом', 2, '[]', 7, 1, '2023-10-29 13:42:53.933119');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (113, '7', 'Платье длинное с разрезом', 2, '[{"changed": {"fields": ["\u0420\u0430\u0437\u043c\u0435\u0440\u044b"]}}]', 7, 1, '2023-10-29 13:43:01.262725');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (114, '7', 'Платье длинное с разрезом', 2, '[{"changed": {"fields": ["\u0420\u0430\u0437\u043c\u0435\u0440\u044b"]}}]', 7, 1, '2023-10-29 13:43:04.193193');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (115, '7', 'Платье длинное с разрезом', 2, '[]', 7, 1, '2023-10-29 13:43:08.357131');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (116, '7', 'Платье длинное с разрезом', 2, '[]', 7, 1, '2023-10-29 13:43:14.994590');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (117, '40', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (59)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (61)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (63)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (65)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (67)"}}]', 8, 1, '2023-10-29 13:43:36.186026');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (118, '39', 'Платье длинное с разрезом - 1003-черный-40-42', 2, '[]', 8, 1, '2023-10-29 13:43:43.265570');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (119, '39', 'Платье длинное с разрезом - 1003-черный-40-42', 2, '[]', 8, 1, '2023-10-29 13:44:01.569021');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (120, '39', 'Платье длинное с разрезом - 1003-черный-40-42', 2, '[{"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (None)"}}]', 8, 1, '2023-10-29 13:46:49.524159');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (121, '39', 'Платье длинное с разрезом - 1003-черный-40-42', 2, '[]', 8, 1, '2023-10-29 13:46:52.773886');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (122, '39', 'Платье длинное с разрезом - 1003-черный-40-42', 2, '[]', 8, 1, '2023-10-29 13:46:59.885546');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (123, '40', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (69)"}}]', 8, 1, '2023-10-29 13:47:19.024223');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (124, '40', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[{"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (None)"}}]', 8, 1, '2023-10-29 13:47:36.446094');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (125, '40', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[]', 8, 1, '2023-10-29 13:47:41.656033');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (126, '39', 'Платье длинное с разрезом - 1003-черный-40-42', 2, '[]', 8, 1, '2023-10-29 13:47:48.919890');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (127, '3', 'Костюмы', 1, '[{"added": {}}]', 9, 1, '2023-10-29 13:48:27.530379');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (128, '8', 'Костюм черный с длинным рукавом', 1, '[{"added": {}}]', 7, 1, '2023-10-29 13:48:49.472254');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (129, '41', 'Костюм черный с длинным рукавом - 1018-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (71)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (72)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (73)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (74)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (75)"}}]', 8, 1, '2023-10-29 13:49:54.003841');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (130, '8', 'Костюм черный с длинным рукавом', 2, '[]', 7, 1, '2023-10-29 13:50:33.096875');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (131, '30', 'Боди черный - 1005-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (76)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (77)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (78)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (79)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (80)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (81)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (82)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (83)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (84)"}}]', 8, 1, '2023-10-29 13:55:34.197495');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (132, '3', 'Костюмы', 2, '[]', 9, 1, '2023-10-29 13:56:28.614675');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (133, '1', 'Платья', 2, '[]', 9, 1, '2023-10-29 13:56:30.258032');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (134, '2', 'Боди', 2, '[]', 9, 1, '2023-10-29 13:56:32.625306');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (135, '8', 'Костюм черный с длинным рукавом', 2, '[]', 7, 1, '2023-10-29 14:02:06.521620');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (136, '4', 'беж', 1, '[{"added": {}}]', 11, 1, '2023-10-29 19:22:10.521192');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (137, '5', 'меланж', 1, '[{"added": {}}]', 11, 1, '2023-10-29 19:22:16.071402');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (138, '9', 'Костюм легкий с коротким рукавом', 1, '[{"added": {}}]', 7, 1, '2023-10-29 19:22:35.591263');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (139, '44', 'Костюм легкий с коротким рукавом - 1013-меланж-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (85)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (86)"}}]', 8, 1, '2023-10-29 19:23:19.336869');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (140, '43', 'Костюм легкий с коротким рукавом - 1013-беж-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (87)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (88)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (89)"}}]', 8, 1, '2023-10-29 19:23:39.451687');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (141, '42', 'Костюм легкий с коротким рукавом - 1013-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (90)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (91)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (92)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (93)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (94)"}}]', 8, 1, '2023-10-29 19:24:00.997102');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (142, '9', 'Костюм легкий с коротким рукавом', 2, '[]', 7, 1, '2023-10-29 19:26:31.617694');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (143, '9', 'Костюм легкий с коротким рукавом', 2, '[]', 7, 1, '2023-10-29 19:26:40.081350');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (144, '6', 'бутылка', 1, '[{"added": {}}]', 11, 1, '2023-10-29 19:32:26.697476');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (145, '7', 'темно-синий', 1, '[{"added": {}}]', 11, 1, '2023-10-29 19:32:35.562569');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (146, '10', 'Платье солнце клеш', 1, '[{"added": {}}]', 7, 1, '2023-10-29 19:32:57.518064');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (147, '50', 'Платье солнце клеш - 435-темно-синий-46-48', 2, '[]', 8, 1, '2023-10-29 19:35:15.413940');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (148, '50', 'Платье солнце клеш - 435-темно-синий-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (95)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (97)"}}]', 8, 1, '2023-10-29 19:35:40.356858');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (149, '48', 'Платье солнце клеш - 435-бутылка-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (99)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (101)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (103)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (105)"}}]', 8, 1, '2023-10-29 19:36:02.175578');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (150, '46', 'Платье солнце клеш - 435-красный-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (107)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (109)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (111)"}}]', 8, 1, '2023-10-29 19:36:14.347791');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (151, '10', 'Платье солнце клеш', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u041f\u043b\u0430\u0442\u044c\u0435 \u0441\u043e\u043b\u043d\u0446\u0435 \u043a\u043b\u0435\u0448 - 435-\u043a\u0440\u0430\u0441\u043d\u044b\u0439-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u041f\u043b\u0430\u0442\u044c\u0435 \u0441\u043e\u043b\u043d\u0446\u0435 \u043a\u043b\u0435\u0448 - 435-\u0431\u0443\u0442\u044b\u043b\u043a\u0430-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u041f\u043b\u0430\u0442\u044c\u0435 \u0441\u043e\u043b\u043d\u0446\u0435 \u043a\u043b\u0435\u0448 - 435-\u0442\u0435\u043c\u043d\u043e-\u0441\u0438\u043d\u0438\u0439-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-10-29 19:36:31.585049');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (152, '8', 'мокко', 1, '[{"added": {}}]', 11, 1, '2023-10-29 19:41:14.989895');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (153, '11', 'Платье рубчик с разрезом', 1, '[{"added": {}}]', 7, 1, '2023-10-29 19:41:42.948943');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (154, '51', 'Платье рубчик с разрезом - 1026-мокко-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (113)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (114)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (115)"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "Image object (116)"}}]', 8, 1, '2023-10-29 19:42:07.044739');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (155, '51', 'Платье рубчик с разрезом - 1026-мокко-42-46', 2, '[]', 8, 1, '2023-10-29 19:44:38.272960');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (156, '12', 'Платье квадратный вырез', 1, '[{"added": {}}]', 7, 1, '2023-10-30 08:35:12.332985');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (157, '53', 'Платье квадратный вырез - 1030-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-35-40.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-35-38.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-35-35.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-35-23.jpg"}}]', 8, 1, '2023-10-30 08:36:10.858346');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (158, '13', 'Платье квадратный разрез длинное', 1, '[{"added": {}}]', 7, 1, '2023-10-30 08:43:01.102601');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (159, '55', 'Платье квадратный разрез длинное - 1029-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-43-30.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-43-28.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-43-26.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-43-23.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-43-16.jpg"}}]', 8, 1, '2023-10-30 08:43:53.942282');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (160, '2', '44', 3, '', 12, 1, '2023-10-30 08:44:51.982281');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (161, '1', '42', 3, '', 12, 1, '2023-10-30 08:44:51.998567');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (162, '14', 'Костюм меланжевый трехнитка', 1, '[{"added": {}}]', 7, 1, '2023-10-30 08:48:56.460515');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (163, '56', 'Костюм меланжевый трехнитка - 1028-меланж-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-49-33.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-49-30.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-49-28.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-49-25.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_10-49-16.jpg"}}]', 8, 1, '2023-10-30 08:49:57.297927');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (164, '3', 'Костюмы', 2, '[]', 9, 1, '2023-10-30 09:44:30.480334');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (165, '9', 'малина', 1, '[{"added": {}}]', 11, 1, '2023-10-30 10:11:18.252725');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (166, '10', 'синий', 1, '[{"added": {}}]', 11, 1, '2023-10-30 10:11:24.003510');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (167, '15', 'Костюм велюровый', 1, '[{"added": {}}]', 7, 1, '2023-10-30 10:11:44.219391');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (168, '58', 'Костюм велюровый - 1021-синий-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_12-10-21.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_12-10-24.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_12-10-26.jpg"}}]', 8, 1, '2023-10-30 10:12:03.106410');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (169, '57', 'Костюм велюровый - 1021-малина-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_12-10-19.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_12-10-12.jpg"}}]', 8, 1, '2023-10-30 10:12:10.810370');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (170, '16', 'Костюм из флиса черный', 1, '[{"added": {}}]', 7, 1, '2023-10-30 15:56:54.370236');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (171, '60', 'Костюм из флиса черный - 1024-черный-48-52', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_17-55-39.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_17-55-54.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_17-55-52.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_17-55-50.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_17-55-47.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_17-55-44.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_17-55-41.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_17-55-31.jpg"}}]', 8, 1, '2023-10-30 15:58:05.953107');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (172, '59', 'Костюм из флиса черный - 1024-черный-42-46', 2, '[]', 8, 1, '2023-10-30 16:29:27.178331');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (173, '60', 'Костюм из флиса черный - 1024-черный-48-52', 2, '[]', 8, 1, '2023-10-30 16:36:58.316662');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (174, '6', 'Платье с длинным рукавом', 2, '[]', 7, 1, '2023-10-30 16:43:56.764009');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (175, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[{"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-49_OIAmkkl.jpg"}}]', 8, 1, '2023-10-30 16:44:27.956376');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (176, '35', 'Платье с длинным рукавом - 411-черный-42-46', 2, '[{"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-49_DC0a4dp.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-46_GIegKbB.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-40_XT5w2UU.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32_S4QPd7Q.jpg"}}]', 8, 1, '2023-10-30 16:45:28.724850');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (177, '35', 'Платье с длинным рукавом - 411-черный-42-46', 2, '[]', 8, 1, '2023-10-30 16:45:30.667729');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (178, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[]', 8, 1, '2023-10-30 16:45:36.724057');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (179, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[]', 8, 1, '2023-10-30 16:45:39.747362');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (180, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[{"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-49.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-46.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-40.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32.jpg"}}]', 8, 1, '2023-10-30 16:46:12.410499');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (181, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-46.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-40.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32_Teg4QEX.jpg"}}]', 8, 1, '2023-10-30 16:47:09.989963');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (182, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[{"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-46.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-40.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32_Teg4QEX.jpg"}}]', 8, 1, '2023-10-30 16:49:16.259604');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (183, '35', 'Платье с длинным рукавом - 411-черный-42-46', 2, '[{"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-46.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-40.jpg"}}, {"deleted": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32_Teg4QEX.jpg"}}]', 8, 1, '2023-10-30 16:49:26.935897');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (184, '35', 'Платье с длинным рукавом - 411-черный-42-46', 2, '[]', 8, 1, '2023-10-30 16:49:28.949769');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (185, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-32.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-40.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-46.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-29_12-21-49.jpg"}}]', 8, 1, '2023-10-30 16:50:17.313213');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (186, '17', 'Костюм кофта и штаны', 1, '[{"added": {}}]', 7, 1, '2023-10-30 16:53:29.547856');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (187, '61', 'Костюм кофта и штаны - 1020-малина-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_18-53-36.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_18-53-45.jpg"}}]', 8, 1, '2023-10-30 16:54:13.029702');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (188, '62', 'Костюм кофта и штаны - 1020-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_18-53-48.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_18-53-51.jpg"}}]', 8, 1, '2023-10-30 16:54:20.727300');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (189, '17', 'Костюм кофта и штаны', 2, '[]', 7, 1, '2023-10-30 19:13:16.869913');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (190, '17', 'Костюм кофта и штаны', 2, '[]', 7, 1, '2023-10-30 19:19:15.040699');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (191, '18', 'Платье с змейкой мангуст', 1, '[{"added": {}}]', 7, 1, '2023-10-30 20:24:16.173308');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (192, '18', 'Платье с змейкой мангуст', 2, '[]', 7, 1, '2023-10-30 20:26:14.549591');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (193, '65', 'Платье с змейкой мангуст - 1023-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-34.jpg"}}]', 8, 1, '2023-10-30 20:27:05.308443');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (194, '64', 'Платье с змейкой мангуст - 1023-малина-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-52.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-49.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-41.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-39.jpg"}}]', 8, 1, '2023-10-30 20:27:20.878686');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (195, '63', 'Платье с змейкой мангуст - 1023-беж-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-54.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-46.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-44.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-26-37.jpg"}}]', 8, 1, '2023-10-30 20:27:40.807645');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (196, '4', 'Юбки', 1, '[{"added": {}}]', 9, 1, '2023-10-30 20:28:26.317882');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (197, '19', 'Юбка черная с вырезом', 1, '[{"added": {}}]', 7, 1, '2023-10-30 20:28:49.411743');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (198, '66', 'Юбка черная с вырезом - 1017-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-29-06.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-29-03.jpg"}}]', 8, 1, '2023-10-30 20:29:14.542032');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (199, '19', 'Юбка черная с вырезом', 2, '[]', 7, 1, '2023-10-30 20:35:53.015282');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (200, '18', 'Платье с змейкой мангуст', 2, '[]', 7, 1, '2023-10-30 20:35:59.346267');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (201, '17', 'Костюм кофта и штаны', 2, '[]', 7, 1, '2023-10-30 20:36:05.522263');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (202, '66', 'Юбка черная с вырезом - 1017-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:36:09.820834');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (203, '66', 'Юбка черная с вырезом - 1017-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:36:13.143571');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (204, '30', 'Боди черный - 1005-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:36:23.096023');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (205, '31', 'Боди черный - 1004-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:36:39.677922');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (206, '30', 'Боди черный - 1005-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:38:01.007840');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (207, '30', 'Боди черный - 1005-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:38:06.905963');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (208, '31', 'Боди черный - 1004-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:38:11.176251');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (209, '31', 'Боди черный - 1004-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:38:17.161931');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (210, '32', 'Боди черный - 1004-черный-48-52', 2, '[]', 8, 1, '2023-10-30 20:38:23.728212');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (211, '32', 'Боди черный - 1004-черный-48-52', 2, '[]', 8, 1, '2023-10-30 20:38:32.460108');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (212, '33', 'Платье белое - 1022-белый-42-44', 2, '[]', 8, 1, '2023-10-30 20:38:40.576193');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (213, '33', 'Платье белое - 1022-белый-42-44', 2, '[]', 8, 1, '2023-10-30 20:38:42.696473');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (214, '34', 'Платье белое - 1022-белый-46-48', 2, '[]', 8, 1, '2023-10-30 20:38:49.536698');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (215, '30', 'Боди черный - 1005-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:40:19.111461');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (216, '65', 'Платье с змейкой мангуст - 1023-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:05.429445');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (217, '65', 'Платье с змейкой мангуст - 1023-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:10.534318');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (218, '64', 'Платье с змейкой мангуст - 1023-малина-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:20.201254');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (219, '63', 'Платье с змейкой мангуст - 1023-беж-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:23.431088');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (220, '62', 'Костюм кофта и штаны - 1020-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:26.375106');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (221, '63', 'Платье с змейкой мангуст - 1023-беж-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:31.505774');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (222, '62', 'Костюм кофта и штаны - 1020-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:35.041550');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (223, '61', 'Костюм кофта и штаны - 1020-малина-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:38.156667');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (224, '60', 'Костюм из флиса черный - 1024-черный-48-52', 2, '[]', 8, 1, '2023-10-30 20:43:42.462152');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (225, '59', 'Костюм из флиса черный - 1024-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:46.454637');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (226, '58', 'Костюм велюровый - 1021-синий-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:49.690628');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (227, '57', 'Костюм велюровый - 1021-малина-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:52.729149');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (228, '56', 'Костюм меланжевый трехнитка - 1028-меланж-42-46', 2, '[]', 8, 1, '2023-10-30 20:43:56.764296');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (229, '55', 'Платье квадратный разрез длинное - 1029-черный-44-46', 2, '[]', 8, 1, '2023-10-30 20:44:00.448321');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (230, '54', 'Платье квадратный разрез длинное - 1029-черный-40-42', 2, '[]', 8, 1, '2023-10-30 20:44:05.166775');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (231, '53', 'Платье квадратный вырез - 1030-черный-44-46', 2, '[]', 8, 1, '2023-10-30 20:44:09.123837');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (232, '52', 'Платье квадратный вырез - 1030-черный-40-42', 2, '[]', 8, 1, '2023-10-30 20:44:13.142187');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (233, '51', 'Платье рубчик с разрезом - 1026-мокко-42-46', 2, '[]', 8, 1, '2023-10-30 20:44:17.688534');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (234, '50', 'Платье солнце клеш - 435-темно-синий-46-48', 2, '[]', 8, 1, '2023-10-30 20:44:21.791582');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (235, '49', 'Платье солнце клеш - 435-темно-синий-42-44', 2, '[]', 8, 1, '2023-10-30 20:44:25.766703');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (236, '48', 'Платье солнце клеш - 435-бутылка-46-48', 2, '[]', 8, 1, '2023-10-30 20:44:31.136776');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (237, '47', 'Платье солнце клеш - 435-бутылка-42-44', 2, '[]', 8, 1, '2023-10-30 20:44:34.823345');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (238, '46', 'Платье солнце клеш - 435-красный-46-48', 2, '[]', 8, 1, '2023-10-30 20:44:38.828143');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (239, '45', 'Платье солнце клеш - 435-красный-42-44', 2, '[]', 8, 1, '2023-10-30 20:44:42.101553');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (240, '44', 'Костюм легкий с коротким рукавом - 1013-меланж-42-46', 2, '[]', 8, 1, '2023-10-30 20:44:46.298256');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (241, '43', 'Костюм легкий с коротким рукавом - 1013-беж-42-46', 2, '[]', 8, 1, '2023-10-30 20:44:50.499022');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (242, '42', 'Костюм легкий с коротким рукавом - 1013-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:44:55.630245');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (243, '41', 'Костюм черный с длинным рукавом - 1018-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:45:03.494832');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (244, '40', 'Платье длинное с разрезом - 1003-черный-44-46', 2, '[]', 8, 1, '2023-10-30 20:45:11.528467');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (245, '36', 'Платье с длинным рукавом - 411-черный-48-52', 2, '[]', 8, 1, '2023-10-30 20:45:18.074137');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (246, '35', 'Платье с длинным рукавом - 411-черный-42-46', 2, '[]', 8, 1, '2023-10-30 20:45:22.393793');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (247, '39', 'Платье длинное с разрезом - 1003-черный-40-42', 2, '[]', 8, 1, '2023-10-30 20:45:57.315375');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (248, '11', 'молоко', 1, '[{"added": {}}]', 11, 1, '2023-10-30 20:51:30.169316');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (249, '20', 'Костюм лосины - кофта мустанг', 1, '[{"added": {}}]', 7, 1, '2023-10-30 20:51:52.063757');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (250, '20', 'Костюм лосины - кофта мустанг', 2, '[]', 7, 1, '2023-10-30 20:52:11.033784');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (251, '72', 'Костюм лосины - кофта мустанг - 448-синий-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-53-09.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-53-07.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-53-05.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-53-02.jpg"}}]', 8, 1, '2023-10-30 20:53:46.526446');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (252, '70', 'Костюм лосины - кофта мустанг - 448-молоко-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-54.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-57.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-59.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-52.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-49.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-39.jpg"}}]', 8, 1, '2023-10-30 20:54:37.519407');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (253, '68', 'Костюм лосины - кофта мустанг - 448-меланж-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-20.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-26.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-28.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-30.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-33.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-30_22-52-35.jpg"}}]', 8, 1, '2023-10-30 20:55:09.700379');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (254, '68', 'Костюм лосины - кофта мустанг - 448-меланж-46-48', 2, '[]', 8, 1, '2023-10-30 20:55:12.026618');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (255, '5', 'Блузки', 1, '[{"added": {}}]', 9, 1, '2023-10-31 17:33:06.825081');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (256, '21', 'Блузка широкий рукав', 1, '[{"added": {}}]', 7, 1, '2023-10-31 17:33:46.364162');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (257, '21', 'Блузка широкий рукав', 2, '[]', 7, 1, '2023-10-31 17:33:54.972924');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (258, '78', 'Блузка широкий рукав - 1014-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-31_19-34-02.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-31_19-34-14.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-31_19-34-17.jpg"}}]', 8, 1, '2023-10-31 17:34:51.818540');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (259, '76', 'Блузка широкий рукав - 1014-красный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-31_19-34-22.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-10-31_19-34-19.jpg"}}]', 8, 1, '2023-10-31 17:35:01.009555');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (260, '1', 'Продажа 1 от 2023-11-01 19:02:58.748316+00:00', 1, '[{"added": {}}]', 13, 1, '2023-11-01 19:02:58.752314');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (261, '1', 'Продажа 1 от 2023-11-01 19:02:58.748316+00:00', 2, '[]', 13, 1, '2023-11-01 19:03:05.624037');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (262, '2', 'Продажа 2 от 2023-11-01 19:04:51.623867+00:00', 1, '[{"added": {}}]', 13, 1, '2023-11-01 19:04:51.627884');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (263, '12', 'Продажа 1, Товар: Блузка широкий рукав, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.612940');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (264, '11', 'Продажа 1, Товар: Блузка широкий рукав, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.623948');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (265, '10', 'Продажа 1, Товар: Блузка широкий рукав, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.635257');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (266, '9', 'Продажа 1, Товар: Блузка широкий рукав, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.645912');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (267, '8', 'Продажа 1, Товар: Блузка широкий рукав, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.657003');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (268, '7', 'Продажа 1, Товар: Блузка широкий рукав, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.668093');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (269, '6', 'Продажа 1, Товар: Костюм лосины - кофта мустанг, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.678756');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (270, '5', 'Продажа 1, Товар: Костюм лосины - кофта мустанг, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.689838');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (271, '4', 'Продажа 1, Товар: Костюм лосины - кофта мустанг, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.700987');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (272, '3', 'Продажа 1, Товар: Костюм лосины - кофта мустанг, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.712252');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (273, '2', 'Продажа 1, Товар: Костюм лосины - кофта мустанг, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.722761');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (274, '1', 'Продажа 1, Товар: Костюм лосины - кофта мустанг, Количество: 1', 3, '', 14, 1, '2023-11-01 19:05:19.732566');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (275, '2', 'Продажа 2 от 2023-11-01 19:04:51.623867+00:00', 2, '[]', 13, 1, '2023-11-01 19:05:33.992443');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (276, '2', 'Продажа 2 от 2023-11-01 19:04:51.623867+00:00', 2, '[{"changed": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u041f\u0440\u043e\u0434\u0430\u0436\u0430 2, \u0422\u043e\u0432\u0430\u0440: \u041a\u043e\u0441\u0442\u044e\u043c \u0432\u0435\u043b\u044e\u0440\u043e\u0432\u044b\u0439, \u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e: 0", "fields": ["\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e"]}}, {"changed": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u041f\u0440\u043e\u0434\u0430\u0436\u0430 2, \u0422\u043e\u0432\u0430\u0440: \u041f\u043b\u0430\u0442\u044c\u0435 \u0441 \u0437\u043c\u0435\u0439\u043a\u043e\u0439 \u043c\u0430\u043d\u0433\u0443\u0441\u0442, \u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e: 0", "fields": ["\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e"]}}]', 13, 1, '2023-11-01 19:05:50.720551');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (277, '2', 'Продажа 2 от 2023-11-01 19:04:51.623867+00:00', 3, '', 13, 1, '2023-11-01 19:06:59.720146');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (278, '1', 'Продажа 1 от 2023-11-01 19:02:58.748316+00:00', 3, '', 13, 1, '2023-11-01 19:06:59.731647');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (279, '3', 'Продажа 3 от 2023-11-01 19:07:12.801171+00:00', 1, '[{"added": {}}]', 13, 1, '2023-11-01 19:07:12.804193');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (280, '3', 'Продажа 3 от 2023-11-01 19:07:12.801171+00:00', 2, '[]', 13, 1, '2023-11-01 19:07:14.848693');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (281, '3', 'Продажа 3 от 2023-11-01 19:07:12.801171+00:00', 2, '[]', 13, 1, '2023-11-01 19:09:14.317212');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (282, '3', 'Продажа 3 от 2023-11-01 19:07:12.801171+00:00', 2, '[]', 13, 1, '2023-11-01 19:09:28.055076');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (283, '3', 'Продажа 3 от 2023-11-01 19:07:12.801171+00:00', 2, '[]', 13, 1, '2023-11-01 19:09:34.560758');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (284, '3', 'Продажа 3 от 2023-11-01 19:07:12.801171+00:00', 3, '', 13, 1, '2023-11-01 19:10:10.747416');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (285, '1', 'Sale #1', 1, '[{"added": {}}]', 13, 1, '2023-11-02 17:49:33.585719');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (286, '1', 'Sale #1', 2, '[{"changed": {"fields": ["\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e"]}}]', 13, 1, '2023-11-02 17:49:40.842189');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (287, '1', 'Sale #1', 2, '[]', 13, 1, '2023-11-02 17:49:41.753823');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (288, '1', 'Продажа #1', 3, '', 13, 1, '2023-11-02 18:06:00.991960');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (289, '2', 'Продажа #2', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #1"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #2"}}]', 13, 1, '2023-11-02 18:06:47.184275');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (290, '3', 'Продажа #3', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #3"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #4"}}]', 13, 1, '2023-11-02 18:11:29.238626');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (291, '3', 'Продажа #3', 3, '', 13, 1, '2023-11-02 18:11:32.767328');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (292, '2', 'Продажа #2', 3, '', 13, 1, '2023-11-02 18:11:32.780358');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (293, '4', 'Продажа #4', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #5"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #6"}}]', 13, 1, '2023-11-02 18:11:41.027392');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (294, '4', 'Продажа #4', 2, '[]', 13, 1, '2023-11-02 18:11:49.048935');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (295, '5', 'Продажа #5', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #7"}}]', 13, 1, '2023-11-02 18:28:33.347567');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (296, '5', 'Продажа #5', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #8"}}]', 13, 1, '2023-11-02 18:35:05.578475');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (297, '5', 'Продажа #5', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #9"}}]', 13, 1, '2023-11-02 18:37:02.719459');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (298, '5', 'Продажа #5', 2, '[]', 13, 1, '2023-11-02 18:42:28.877516');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (299, '6', 'Продажа #6', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #10"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #11"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #12"}}]', 13, 1, '2023-11-02 18:54:30.144446');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (300, '6', 'Продажа #6', 2, '[]', 13, 1, '2023-11-02 19:03:30.919110');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (301, '6', 'Продажа #6', 2, '[]', 13, 1, '2023-11-02 19:09:05.838145');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (302, '6', 'Продажа #6', 3, '', 13, 1, '2023-11-02 19:09:10.408621');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (303, '5', 'Продажа #5', 3, '', 13, 1, '2023-11-02 19:09:10.420722');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (304, '4', 'Продажа #4', 3, '', 13, 1, '2023-11-02 19:09:10.435301');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (305, '7', 'Продажа #7', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #13"}}]', 13, 1, '2023-11-02 19:09:41.018588');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (306, '7', 'Продажа #7', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #14"}}]', 13, 1, '2023-11-02 19:10:00.696122');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (307, '7', 'Продажа #7', 2, '[]', 13, 1, '2023-11-02 19:14:41.526516');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (308, '7', 'Продажа #7', 2, '[]', 13, 1, '2023-11-02 19:15:03.478772');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (309, '7', 'Продажа #7', 2, '[]', 13, 1, '2023-11-02 19:15:21.289191');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (310, '7', 'Продажа #7', 2, '[]', 13, 1, '2023-11-02 19:15:26.794705');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (311, '8', 'Продажа #8', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #15"}}]', 13, 1, '2023-11-02 19:17:05.588807');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (312, '8', 'Продажа #8', 2, '[]', 13, 1, '2023-11-02 19:17:41.987254');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (313, '8', 'Продажа #8', 2, '[]', 13, 1, '2023-11-02 19:17:54.398949');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (314, '12', 'голубой', 1, '[{"added": {}}]', 11, 1, '2023-11-02 19:23:22.793969');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (315, '9', '42-50', 1, '[{"added": {}}]', 12, 1, '2023-11-02 19:23:36.589545');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (316, '22', 'Рубашка женская', 1, '[{"added": {}}]', 7, 1, '2023-11-02 19:23:49.666051');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (317, '80', '465-голубой-42-50', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-02_21-22-48.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-02_21-22-46.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-02_21-22-43.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-02_21-22-41.jpg"}}]', 8, 1, '2023-11-02 19:24:24.192007');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (318, '79', '465-белый-42-50', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-02_21-22-39.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-02_21-22-37.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-02_21-22-34.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-02_21-22-26.jpg"}}]', 8, 1, '2023-11-02 19:24:39.417727');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (319, '13', 'шоколад', 1, '[{"added": {}}]', 11, 1, '2023-11-03 19:14:28.269253');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (320, '23', 'Платье с вырезом', 1, '[{"added": {}}]', 7, 1, '2023-11-03 19:14:41.853678');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (321, '82', '1019-шоколад-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-13-32.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-13-40.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-13-43.jpg"}}]', 8, 1, '2023-11-03 19:15:14.503185');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (322, '81', '1019-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-13-48.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-13-45.jpg"}}]', 8, 1, '2023-11-03 19:15:22.903040');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (323, '24', 'Топ с длинным рукавом', 1, '[{"added": {}}]', 7, 1, '2023-11-03 19:16:33.934194');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (324, '83', '1027-черный-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-16-47.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-16-44.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-16-41.jpg"}}]', 8, 1, '2023-11-03 19:16:59.504465');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (325, '25', 'Платье квадратный вырез', 1, '[{"added": {}}]', 7, 1, '2023-11-03 19:21:55.112458');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (326, '85', '1002-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-20-57.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-20-55.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-20-53.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-03_21-20-45.jpg"}}]', 8, 1, '2023-11-03 19:22:35.954257');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (327, '8', 'Продажа #8', 3, '', 13, 1, '2023-11-04 11:03:56.174323');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (328, '7', 'Продажа #7', 3, '', 13, 1, '2023-11-04 11:03:56.187331');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (329, '25', 'Платье квадратный вырез', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-40-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-44-46", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-04 11:04:06.707608');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (330, '9', 'Продажа #9', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #16"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #17"}}]', 13, 1, '2023-11-04 11:04:42.420490');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (331, '9', 'Продажа #9', 2, '[]', 13, 1, '2023-11-04 11:04:53.216828');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (332, '9', 'Продажа #9', 2, '[]', 13, 1, '2023-11-04 11:04:57.536398');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (333, '9', 'Продажа #9', 2, '[]', 13, 1, '2023-11-04 11:05:49.842016');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (334, '10', 'Продажа #10', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #18"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #19"}}]', 13, 1, '2023-11-04 11:06:37.961937');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (335, '10', 'Продажа #10', 3, '', 13, 1, '2023-11-04 11:07:53.105725');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (336, '9', 'Продажа #9', 3, '', 13, 1, '2023-11-04 11:07:53.120876');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (337, '11', 'Продажа #11', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #20"}}]', 13, 1, '2023-11-04 11:07:59.781860');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (338, '11', 'Продажа #11', 2, '[]', 13, 1, '2023-11-04 11:08:20.113316');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (339, '11', 'Продажа #11', 2, '[]', 13, 1, '2023-11-04 11:08:34.546851');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (340, '11', 'Продажа #11', 2, '[]', 13, 1, '2023-11-04 11:08:54.352385');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (341, '11', 'Продажа #11', 2, '[]', 13, 1, '2023-11-04 11:09:52.970849');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (342, '12', 'Продажа #12', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #21"}}]', 13, 1, '2023-11-04 11:11:34.421756');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (343, '12', 'Продажа #12', 2, '[{"changed": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #21", "fields": ["\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e"]}}]', 13, 1, '2023-11-04 11:11:52.937470');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (344, '12', 'Продажа #12', 2, '[]', 13, 1, '2023-11-04 11:12:04.913809');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (345, '12', 'Продажа #12', 2, '[]', 13, 1, '2023-11-04 11:12:09.337776');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (346, '13', 'Продажа #13', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #22"}}]', 13, 1, '2023-11-04 11:12:17.277836');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (347, '13', 'Продажа #13', 2, '[]', 13, 1, '2023-11-04 11:12:21.982856');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (348, '14', 'Продажа #14', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #23"}}]', 13, 1, '2023-11-04 11:12:31.547252');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (349, '14', 'Продажа #14', 3, '', 13, 1, '2023-11-04 11:12:48.982739');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (350, '13', 'Продажа #13', 3, '', 13, 1, '2023-11-04 11:12:48.991994');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (351, '12', 'Продажа #12', 3, '', 13, 1, '2023-11-04 11:12:48.999412');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (352, '11', 'Продажа #11', 3, '', 13, 1, '2023-11-04 11:12:49.010922');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (353, '15', 'Продажа #15', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #24"}}]', 13, 1, '2023-11-04 11:17:32.529397');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (354, '15', 'Продажа #15', 2, '[]', 13, 1, '2023-11-04 11:17:37.102161');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (355, '15', 'Продажа #15', 3, '', 13, 1, '2023-11-04 11:17:52.475371');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (356, '25', 'Платье квадратный вырез', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-40-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-04 11:17:59.114011');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (357, '16', 'Продажа #16', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #25"}}]', 13, 1, '2023-11-04 11:18:06.860005');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (358, '16', 'Продажа #16', 3, '', 13, 1, '2023-11-04 11:18:45.111157');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (359, '17', 'Продажа #17', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #26"}}]', 13, 1, '2023-11-04 11:22:34.863600');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (360, '17', 'Продажа #17', 2, '[]', 13, 1, '2023-11-04 11:22:36.806876');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (361, '18', 'Продажа #18', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #27"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #28"}}]', 13, 1, '2023-11-04 11:23:07.223696');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (362, '18', 'Продажа #18', 3, '', 13, 1, '2023-11-04 11:24:40.384062');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (363, '17', 'Продажа #17', 3, '', 13, 1, '2023-11-04 11:24:40.395926');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (364, '19', 'Продажа #19', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #29"}}]', 13, 1, '2023-11-04 11:24:51.132153');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (365, '19', 'Продажа #19', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #30"}}]', 13, 1, '2023-11-04 11:25:11.237534');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (366, '19', 'Продажа #19', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #31"}}]', 13, 1, '2023-11-04 14:29:47.995846');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (367, '19', 'Продажа #19', 3, '', 13, 1, '2023-11-04 14:29:52.125993');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (368, '20', 'Продажа #20', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #32"}}]', 13, 1, '2023-11-04 14:36:54.133410');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (369, '20', 'Продажа #20', 3, '', 13, 1, '2023-11-04 14:50:17.397259');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (370, '21', 'Продажа #21', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #33"}}]', 13, 1, '2023-11-04 14:50:31.819891');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (371, '22', 'Продажа #22', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #34"}}]', 13, 1, '2023-11-04 14:51:02.541490');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (372, '23', 'Продажа #23', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #35"}}]', 13, 1, '2023-11-04 14:52:33.439601');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (373, '24', 'Продажа #24', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #36"}}]', 13, 1, '2023-11-04 14:52:57.204853');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (374, '25', 'Продажа #25', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #37"}}]', 13, 1, '2023-11-04 14:56:15.330466');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (375, '26', 'Продажа #26', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #38"}}]', 13, 1, '2023-11-04 14:56:55.425972');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (376, '27', 'Продажа #27', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #39"}}]', 13, 1, '2023-11-04 14:57:26.949007');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (377, '27', 'Продажа #27', 2, '[]', 13, 1, '2023-11-04 14:57:52.643981');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (378, '27', 'Продажа #27', 3, '', 13, 1, '2023-11-04 15:03:30.986307');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (379, '26', 'Продажа #26', 3, '', 13, 1, '2023-11-04 15:03:30.999011');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (380, '25', 'Продажа #25', 3, '', 13, 1, '2023-11-04 15:03:31.009106');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (381, '24', 'Продажа #24', 3, '', 13, 1, '2023-11-04 15:03:31.020160');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (382, '23', 'Продажа #23', 3, '', 13, 1, '2023-11-04 15:03:31.030233');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (383, '22', 'Продажа #22', 3, '', 13, 1, '2023-11-04 15:03:31.040431');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (384, '21', 'Продажа #21', 3, '', 13, 1, '2023-11-04 15:03:31.050942');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (385, '28', 'Продажа #28', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #40"}}]', 13, 1, '2023-11-04 15:10:41.918883');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (386, '28', 'Продажа #28', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #41"}}]', 13, 1, '2023-11-04 15:11:35.051243');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (387, '28', 'Продажа #28', 3, '', 13, 1, '2023-11-04 16:30:46.293966');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (388, '29', 'Продажа #29', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #42"}}]', 13, 1, '2023-11-04 16:32:23.458000');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (389, '30', 'Продажа #30', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #43"}}]', 13, 1, '2023-11-04 16:37:44.890199');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (390, '31', 'Продажа #31', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #44"}}]', 13, 1, '2023-11-04 16:38:40.962155');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (391, '31', 'Продажа #31', 2, '[]', 13, 1, '2023-11-04 16:38:47.554314');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (392, '31', 'Продажа #31', 2, '[]', 13, 1, '2023-11-04 16:38:50.048382');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (393, '32', 'Продажа #32', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #45"}}]', 13, 1, '2023-11-04 16:38:59.866489');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (394, '33', 'Продажа #33', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #46"}}]', 13, 1, '2023-11-04 16:39:29.343422');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (395, '34', 'Продажа #34', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #47"}}]', 13, 1, '2023-11-04 16:39:46.458375');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (396, '35', 'Продажа #35', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #48"}}]', 13, 1, '2023-11-04 16:40:07.086130');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (397, '36', 'Продажа #36', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #49"}}]', 13, 1, '2023-11-04 16:41:28.000525');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (398, '37', 'Продажа #37', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #50"}}]', 13, 1, '2023-11-04 16:41:57.782930');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (399, '38', 'Продажа #38', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #51"}}]', 13, 1, '2023-11-04 16:45:52.507706');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (400, '39', 'Продажа #39', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #52"}}]', 13, 1, '2023-11-04 16:47:56.168444');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (401, '40', 'Продажа #40', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #53"}}]', 13, 1, '2023-11-04 16:48:11.373820');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (402, '40', 'Продажа #40', 3, '', 13, 1, '2023-11-05 08:02:44.310360');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (403, '39', 'Продажа #39', 3, '', 13, 1, '2023-11-05 08:02:44.322380');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (404, '38', 'Продажа #38', 3, '', 13, 1, '2023-11-05 08:02:44.332762');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (405, '37', 'Продажа #37', 3, '', 13, 1, '2023-11-05 08:02:44.342788');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (406, '36', 'Продажа #36', 3, '', 13, 1, '2023-11-05 08:02:44.353669');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (407, '35', 'Продажа #35', 3, '', 13, 1, '2023-11-05 08:02:44.364667');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (408, '34', 'Продажа #34', 3, '', 13, 1, '2023-11-05 08:02:44.374600');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (409, '33', 'Продажа #33', 3, '', 13, 1, '2023-11-05 08:02:44.384142');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (410, '32', 'Продажа #32', 3, '', 13, 1, '2023-11-05 08:02:44.395121');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (411, '31', 'Продажа #31', 3, '', 13, 1, '2023-11-05 08:02:44.405025');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (412, '30', 'Продажа #30', 3, '', 13, 1, '2023-11-05 08:02:44.415523');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (413, '29', 'Продажа #29', 3, '', 13, 1, '2023-11-05 08:02:44.426253');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (414, '41', 'Продажа #41', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #54"}}]', 13, 1, '2023-11-05 08:06:04.350364');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (415, '41', 'Продажа #41', 2, '[]', 13, 1, '2023-11-05 08:06:29.005907');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (416, '41', 'Продажа #41', 2, '[]', 13, 1, '2023-11-05 08:06:32.606669');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (417, '41', 'Продажа #41', 2, '[]', 13, 1, '2023-11-05 08:06:34.194000');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (418, '41', 'Продажа #41', 3, '', 13, 1, '2023-11-05 08:33:25.143138');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (419, '42', 'Продажа #42', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #55"}}]', 13, 1, '2023-11-05 08:33:44.676261');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (420, '42', 'Продажа #42', 2, '[]', 13, 1, '2023-11-05 08:33:49.348897');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (421, '42', 'Продажа #42', 2, '[]', 13, 1, '2023-11-05 08:33:51.517480');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (422, '43', 'Продажа #43', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #56"}}]', 13, 1, '2023-11-05 08:54:53.280462');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (423, '44', 'Продажа #44', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #57"}}]', 13, 1, '2023-11-05 08:58:16.462903');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (424, '44', 'Продажа #44', 2, '[]', 13, 1, '2023-11-05 08:58:22.103979');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (425, '45', 'Продажа #45', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #58"}}]', 13, 1, '2023-11-05 11:47:28.265112');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (426, '45', 'Продажа #45', 2, '[]', 13, 1, '2023-11-05 11:47:33.942063');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (427, '45', 'Продажа #45', 2, '[]', 13, 1, '2023-11-05 11:47:41.150999');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (428, '25', 'Платье квадратный вырез', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-40-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-44-46", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-05 11:55:54.334128');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (429, '46', 'Продажа #46', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #59"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #60"}}]', 13, 1, '2023-11-05 11:56:08.121103');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (430, '46', 'Продажа #46', 3, '', 13, 1, '2023-11-05 12:09:31.064420');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (431, '45', 'Продажа #45', 3, '', 13, 1, '2023-11-05 12:09:31.075058');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (432, '44', 'Продажа #44', 3, '', 13, 1, '2023-11-05 12:09:31.085292');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (433, '43', 'Продажа #43', 3, '', 13, 1, '2023-11-05 12:09:31.095042');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (434, '42', 'Продажа #42', 3, '', 13, 1, '2023-11-05 12:09:31.106121');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (435, '47', 'Продажа #47', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #61"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #62"}}]', 13, 1, '2023-11-05 12:10:13.023141');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (436, '47', 'Продажа #47', 2, '[]', 13, 1, '2023-11-05 12:10:20.131877');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (437, '47', 'Продажа #47', 3, '', 13, 1, '2023-11-05 12:14:27.272827');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (438, '48', 'Продажа #48', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #63"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #64"}}]', 13, 1, '2023-11-05 12:14:38.826515');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (439, '48', 'Продажа #48', 2, '[]', 13, 1, '2023-11-05 12:14:49.493114');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (440, '48', 'Продажа #48', 2, '[]', 13, 1, '2023-11-05 12:14:55.723158');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (441, '48', 'Продажа #48', 2, '[]', 13, 1, '2023-11-05 12:15:02.154263');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (442, '48', 'Продажа #48', 3, '', 13, 1, '2023-11-05 12:15:44.747280');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (443, '49', 'Продажа #49', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #65"}}]', 13, 1, '2023-11-05 12:16:10.634038');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (444, '49', 'Продажа #49', 2, '[{"deleted": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #None"}}]', 13, 1, '2023-11-05 12:16:18.628658');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (445, '49', 'Продажа #49', 3, '', 13, 1, '2023-11-05 12:18:15.073677');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (446, '25', 'Платье квадратный вырез', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-40-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-44-46", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-05 12:18:26.799468');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (447, '50', 'Продажа #50', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #66"}}]', 13, 1, '2023-11-05 12:18:34.757532');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (448, '50', 'Продажа #50', 2, '[]', 13, 1, '2023-11-05 12:18:48.158311');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (449, '50', 'Продажа #50', 3, '', 13, 1, '2023-11-05 12:18:57.760051');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (450, '51', 'Продажа #51', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #67"}}]', 13, 1, '2023-11-05 12:19:11.157079');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (451, '51', 'Продажа #51', 2, '[{"deleted": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #None"}}]', 13, 1, '2023-11-05 12:19:15.331921');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (452, '51', 'Продажа #51', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #68"}}]', 13, 1, '2023-11-05 12:19:19.658995');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (453, '51', 'Продажа #51', 3, '', 13, 1, '2023-11-05 13:23:02.344779');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (454, '52', 'Продажа #52', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #69"}}]', 13, 1, '2023-11-05 13:23:19.616840');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (455, '52', 'Продажа #52', 2, '[]', 13, 1, '2023-11-05 13:23:25.668452');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (456, '52', 'Продажа #52', 2, '[]', 13, 1, '2023-11-05 13:23:29.607253');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (457, '52', 'Продажа #52', 2, '[]', 13, 1, '2023-11-05 13:23:34.341278');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (458, '52', 'Продажа #52', 2, '[]', 13, 1, '2023-11-05 13:23:42.833099');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (459, '52', 'Продажа #52', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #70"}}]', 13, 1, '2023-11-05 13:23:58.034334');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (460, '52', 'Продажа #52', 2, '[{"deleted": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #None"}}, {"deleted": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #None"}}]', 13, 1, '2023-11-05 13:24:05.234083');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (461, '52', 'Продажа #52', 2, '[]', 13, 1, '2023-11-05 13:24:09.806818');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (462, '25', 'Платье квадратный вырез', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-40-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-44-46", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-05 13:24:26.269712');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (463, '52', 'Продажа #52', 3, '', 13, 1, '2023-11-05 13:24:35.460811');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (464, '53', 'Продажа #53', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #71"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #72"}}]', 13, 1, '2023-11-05 13:24:47.319978');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (465, '53', 'Продажа #53', 2, '[{"deleted": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #None"}}]', 13, 1, '2023-11-05 13:27:46.938271');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (466, '53', 'Продажа #53', 2, '[]', 13, 1, '2023-11-05 13:27:49.365006');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (467, '54', 'Продажа #54', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #73"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #74"}}]', 13, 1, '2023-11-05 13:31:18.476338');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (468, '54', 'Продажа #54', 2, '[]', 13, 1, '2023-11-05 14:01:38.085147');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (469, '54', 'Продажа #54', 2, '[]', 13, 1, '2023-11-05 14:01:41.975811');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (470, '54', 'Продажа #54', 2, '[]', 13, 1, '2023-11-05 14:01:48.056696');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (471, '54', 'Продажа #54', 2, '[]', 13, 1, '2023-11-05 14:01:52.204900');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (472, '55', 'Продажа #55', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #75"}}]', 13, 1, '2023-11-05 14:01:56.907336');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (473, '55', 'Продажа #55', 2, '[]', 13, 1, '2023-11-05 14:01:59.363588');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (474, '55', 'Продажа #55', 3, '', 13, 1, '2023-11-05 14:02:10.345207');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (475, '54', 'Продажа #54', 3, '', 13, 1, '2023-11-05 14:02:10.356557');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (476, '53', 'Продажа #53', 3, '', 13, 1, '2023-11-05 14:02:10.368064');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (477, '25', 'Платье квадратный вырез', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-40-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-44-46", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-05 14:02:24.390289');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (478, '56', 'Продажа #56', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #76"}}]', 13, 1, '2023-11-05 14:02:30.280562');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (479, '56', 'Продажа #56', 2, '[]', 13, 1, '2023-11-05 14:02:32.027592');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (480, '56', 'Продажа #56', 2, '[{"deleted": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #None"}}]', 13, 1, '2023-11-05 14:02:41.027497');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (481, '56', 'Продажа #56', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #77"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #78"}}]', 13, 1, '2023-11-05 14:02:59.177261');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (482, '56', 'Продажа #56', 2, '[{"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #79"}}]', 13, 1, '2023-11-05 14:03:27.972716');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (483, '56', 'Продажа #56', 2, '[]', 13, 1, '2023-11-05 14:03:39.328055');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (484, '57', 'Продажа #57', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #80"}}]', 13, 1, '2023-11-05 14:03:51.020199');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (485, '57', 'Продажа #57', 3, '', 13, 1, '2023-11-05 14:31:41.594451');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (486, '56', 'Продажа #56', 3, '', 13, 1, '2023-11-05 14:31:41.604687');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (487, '25', 'Платье квадратный вырез', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-40-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-44-46", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-05 14:31:53.824273');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (488, '58', 'Продажа #58', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #81"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #82"}}]', 13, 1, '2023-11-05 14:32:05.990381');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (489, '59', 'Продажа #59', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #83"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #84"}}]', 13, 1, '2023-11-05 14:32:32.155876');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (490, '59', 'Продажа #59', 2, '[]', 13, 1, '2023-11-05 14:32:34.814690');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (491, '59', 'Продажа #59', 3, '', 13, 1, '2023-11-05 14:32:56.806312');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (492, '58', 'Продажа #58', 3, '', 13, 1, '2023-11-05 14:32:56.818383');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (493, '60', 'Продажа #60', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #85"}}]', 13, 1, '2023-11-05 14:33:06.733583');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (494, '60', 'Продажа #60', 3, '', 13, 1, '2023-11-05 14:36:32.644954');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (495, '61', 'Продажа #61', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #86"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #87"}}]', 13, 1, '2023-11-05 14:36:43.458560');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (496, '61', 'Продажа #61', 2, '[]', 13, 1, '2023-11-05 14:36:47.453607');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (497, '61', 'Продажа #61', 3, '', 13, 1, '2023-11-05 15:29:40.361961');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (498, '62', 'Продажа #62', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #88"}}]', 13, 1, '2023-11-05 15:29:46.551969');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (499, '63', 'Продажа #63', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #89"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #90"}}]', 13, 1, '2023-11-05 15:30:21.152496');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (500, '64', 'Продажа #64', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #91"}}]', 13, 1, '2023-11-05 15:32:18.343480');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (501, '64', 'Продажа #64', 3, '', 13, 1, '2023-11-05 15:32:39.416798');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (502, '63', 'Продажа #63', 3, '', 13, 1, '2023-11-05 15:34:15.959396');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (503, '25', 'Платье квадратный вырез', 2, '[]', 7, 1, '2023-11-05 15:34:23.131960');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (504, '65', 'Продажа #65', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #92"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #93"}}]', 13, 1, '2023-11-05 15:34:32.446380');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (505, '65', 'Продажа #65', 3, '', 13, 1, '2023-11-05 15:38:59.542550');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (506, '62', 'Продажа #62', 3, '', 13, 1, '2023-11-05 15:38:59.554704');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (507, '66', 'Продажа #66', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #94"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #95"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #96"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #97"}}]', 13, 1, '2023-11-05 15:39:13.902395');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (508, '67', 'Продажа #67', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #98"}}]', 13, 1, '2023-11-05 15:45:04.672193');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (509, '25', 'Платье квадратный вырез', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-40-42", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "1002-\u0447\u0435\u0440\u043d\u044b\u0439-44-46", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-05 16:36:20.946811');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (510, '68', 'Продажа #68', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #99"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #100"}}]', 13, 1, '2023-11-05 16:36:36.001903');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (511, '68', 'Продажа #68', 3, '', 13, 1, '2023-11-05 16:36:46.246076');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (512, '67', 'Продажа #67', 3, '', 13, 1, '2023-11-05 16:36:46.258652');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (513, '66', 'Продажа #66', 3, '', 13, 1, '2023-11-05 16:36:46.269797');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (514, '25', 'Платье квадратный вырез', 2, '[]', 7, 1, '2023-11-05 16:36:52.781064');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (515, '69', 'Продажа #69', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #101"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #102"}}]', 13, 1, '2023-11-05 16:58:59.383981');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (516, '1', 'Возврат #1', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 #1"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 #2"}}]', 15, 1, '2023-11-06 11:04:12.523675');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (517, '1', 'Возврат #1', 3, '', 15, 1, '2023-11-06 11:11:14.050914');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (518, '69', 'Продажа #69', 3, '', 13, 1, '2023-11-06 11:14:34.744829');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (519, '70', 'Продажа #70', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #103"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #104"}}]', 13, 1, '2023-11-06 11:14:55.623411');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (520, '2', 'Возврат #2', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 #3"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 #4"}}]', 15, 1, '2023-11-06 11:15:24.013025');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (521, '2', 'Возврат #2', 3, '', 15, 1, '2023-11-06 11:15:43.240497');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (522, '70', 'Продажа #70', 3, '', 13, 1, '2023-11-06 11:15:52.085064');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (523, '3', 'Возврат #3', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 #5"}}]', 15, 1, '2023-11-06 11:18:58.982380');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (524, '71', 'Продажа #71', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #105"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #106"}}]', 13, 1, '2023-11-06 11:19:32.627051');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (525, '26', 'Платье малина миди с вырезом', 1, '[{"added": {}}]', 7, 1, '2023-11-07 18:40:36.841297');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (526, '26', 'Платье малина миди с вырезом', 2, '[]', 7, 1, '2023-11-07 18:40:40.038921');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (527, '86', '1031-меланж-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-06_20-40-16.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-06_20-40-12.jpg"}}]', 8, 1, '2023-11-07 18:41:27.551843');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (528, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-09 17:57:26.034372');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (529, '1', 'Arg??', 2, '[]', 18, 1, '2023-11-09 17:57:45.582344');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (530, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-09 18:11:11.273293');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (531, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-09 19:33:27.537168');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (532, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-09 19:33:42.054697');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (533, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-09 19:45:32.434012');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (534, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-09 19:49:51.347318');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (535, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-09 19:50:12.345790');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (536, '72', 'Продажа #72', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #107"}}]', 13, 1, '2023-11-09 19:59:41.294983');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (537, '1', 'Arg??', 2, '[]', 18, 1, '2023-11-09 19:59:57.837932');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (538, '76', 'Продажа #76', 3, '', 13, 1, '2023-11-10 15:57:40.236091');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (539, '75', 'Продажа #75', 3, '', 13, 1, '2023-11-10 15:57:40.248098');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (540, '74', 'Продажа #74', 3, '', 13, 1, '2023-11-10 15:57:40.259109');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (541, '73', 'Продажа #73', 3, '', 13, 1, '2023-11-10 15:57:40.270111');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (542, '72', 'Продажа #72', 3, '', 13, 1, '2023-11-10 15:57:40.279849');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (543, '71', 'Продажа #71', 3, '', 13, 1, '2023-11-10 15:57:40.290861');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (544, '77', 'Продажа #77', 3, '', 13, 1, '2023-11-10 15:59:23.455456');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (545, '79', 'Продажа #79', 3, '', 13, 1, '2023-11-10 16:01:02.359344');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (546, '78', 'Продажа #78', 3, '', 13, 1, '2023-11-10 16:01:02.371345');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (547, '81', 'Продажа #81', 3, '', 13, 1, '2023-11-10 16:01:51.834597');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (548, '80', 'Продажа #80', 3, '', 13, 1, '2023-11-10 16:01:51.847663');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (549, '85', 'Продажа #85', 3, '', 13, 1, '2023-11-10 16:03:56.832549');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (550, '84', 'Продажа #84', 3, '', 13, 1, '2023-11-10 16:03:56.843612');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (551, '83', 'Продажа #83', 3, '', 13, 1, '2023-11-10 16:03:56.854604');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (552, '82', 'Продажа #82', 3, '', 13, 1, '2023-11-10 16:03:56.865605');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (553, '92', 'Продажа #92', 3, '', 13, 1, '2023-11-10 16:41:10.211234');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (554, '91', 'Продажа #91', 3, '', 13, 1, '2023-11-10 16:41:10.223304');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (555, '90', 'Продажа #90', 3, '', 13, 1, '2023-11-10 16:41:10.235003');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (556, '89', 'Продажа #89', 3, '', 13, 1, '2023-11-10 16:41:10.245390');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (557, '88', 'Продажа #88', 3, '', 13, 1, '2023-11-10 16:41:10.256925');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (558, '87', 'Продажа #87', 3, '', 13, 1, '2023-11-10 16:41:10.266933');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (559, '86', 'Продажа #86', 3, '', 13, 1, '2023-11-10 16:41:10.279108');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (560, '93', 'Продажа #93', 3, '', 13, 1, '2023-11-10 16:41:15.495781');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (561, '96', 'Продажа #96', 3, '', 13, 1, '2023-11-10 16:44:58.568179');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (562, '95', 'Продажа #95', 3, '', 13, 1, '2023-11-10 16:44:58.581207');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (563, '94', 'Продажа #94', 3, '', 13, 1, '2023-11-10 16:44:58.595234');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (564, '14', 'горчица', 1, '[{"added": {}}]', 11, 1, '2023-11-11 10:01:26.337129');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (565, '27', 'Платье с вырезом из дайвинга миди', 1, '[{"added": {}}]', 7, 1, '2023-11-11 10:01:52.306416');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (566, '92', '447-красный-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-11_12-00-35.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-11_12-00-37.jpg"}}]', 8, 1, '2023-11-11 10:02:08.956017');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (567, '90', '447-горчица-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-11_12-00-30.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-11_12-00-32.jpg"}}]', 8, 1, '2023-11-11 10:02:17.706774');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (568, '88', '447-бутылка-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-11_12-00-19.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-11_12-00-27.jpg"}}]', 8, 1, '2023-11-11 10:02:27.239163');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (569, '27', 'Платье с вырезом из дайвинга миди', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u0431\u0443\u0442\u044b\u043b\u043a\u0430-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u0431\u0443\u0442\u044b\u043b\u043a\u0430-46-48", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u0433\u043e\u0440\u0447\u0438\u0446\u0430-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u0433\u043e\u0440\u0447\u0438\u0446\u0430-46-48", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u043a\u0440\u0430\u0441\u043d\u044b\u0439-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-11 10:02:48.214084');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (570, '27', 'Платье с вырезом из дайвинга миди', 2, '[{"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u0431\u0443\u0442\u044b\u043b\u043a\u0430-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u0431\u0443\u0442\u044b\u043b\u043a\u0430-46-48", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u0433\u043e\u0440\u0447\u0438\u0446\u0430-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u0433\u043e\u0440\u0447\u0438\u0446\u0430-46-48", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u043a\u0440\u0430\u0441\u043d\u044b\u0439-42-44", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}, {"changed": {"name": "\u041c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "447-\u043a\u0440\u0430\u0441\u043d\u044b\u0439-46-48", "fields": ["\u041e\u0441\u0442\u0430\u0442\u043e\u043a"]}}]', 7, 1, '2023-11-11 11:01:10.968438');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (571, '155', 'Продажа #155', 3, '', 13, 1, '2023-11-11 12:28:54.838551');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (572, '154', 'Продажа #154', 3, '', 13, 1, '2023-11-11 12:28:54.853087');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (573, '153', 'Продажа #153', 3, '', 13, 1, '2023-11-11 12:28:54.865276');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (574, '152', 'Продажа #152', 3, '', 13, 1, '2023-11-11 12:28:54.878326');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (575, '151', 'Продажа #151', 3, '', 13, 1, '2023-11-11 12:28:54.895366');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (576, '150', 'Продажа #150', 3, '', 13, 1, '2023-11-11 12:28:54.912876');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (577, '149', 'Продажа #149', 3, '', 13, 1, '2023-11-11 12:28:54.927530');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (578, '148', 'Продажа #148', 3, '', 13, 1, '2023-11-11 12:28:54.941899');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (579, '147', 'Продажа #147', 3, '', 13, 1, '2023-11-11 12:28:54.954409');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (580, '146', 'Продажа #146', 3, '', 13, 1, '2023-11-11 12:28:54.966416');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (581, '145', 'Продажа #145', 3, '', 13, 1, '2023-11-11 12:28:54.978714');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (582, '144', 'Продажа #144', 3, '', 13, 1, '2023-11-11 12:28:54.991804');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (583, '143', 'Продажа #143', 3, '', 13, 1, '2023-11-11 12:28:55.004326');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (584, '142', 'Продажа #142', 3, '', 13, 1, '2023-11-11 12:28:55.016839');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (585, '141', 'Продажа #141', 3, '', 13, 1, '2023-11-11 12:28:55.028844');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (586, '140', 'Продажа #140', 3, '', 13, 1, '2023-11-11 12:28:55.042287');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (587, '139', 'Продажа #139', 3, '', 13, 1, '2023-11-11 12:28:55.058136');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (588, '138', 'Продажа #138', 3, '', 13, 1, '2023-11-11 12:28:55.075146');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (589, '137', 'Продажа #137', 3, '', 13, 1, '2023-11-11 12:28:55.088709');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (590, '136', 'Продажа #136', 3, '', 13, 1, '2023-11-11 12:28:55.105809');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (591, '135', 'Продажа #135', 3, '', 13, 1, '2023-11-11 12:28:55.122322');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (592, '134', 'Продажа #134', 3, '', 13, 1, '2023-11-11 12:28:55.136371');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (593, '133', 'Продажа #133', 3, '', 13, 1, '2023-11-11 12:28:55.152766');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (594, '132', 'Продажа #132', 3, '', 13, 1, '2023-11-11 12:28:55.167295');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (595, '131', 'Продажа #131', 3, '', 13, 1, '2023-11-11 12:28:55.180804');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (596, '130', 'Продажа #130', 3, '', 13, 1, '2023-11-11 12:28:55.194318');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (597, '129', 'Продажа #129', 3, '', 13, 1, '2023-11-11 12:28:55.209199');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (598, '128', 'Продажа #128', 3, '', 13, 1, '2023-11-11 12:28:55.221254');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (599, '127', 'Продажа #127', 3, '', 13, 1, '2023-11-11 12:28:55.232651');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (600, '126', 'Продажа #126', 3, '', 13, 1, '2023-11-11 12:28:55.247470');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (601, '125', 'Продажа #125', 3, '', 13, 1, '2023-11-11 12:28:55.261488');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (602, '124', 'Продажа #124', 3, '', 13, 1, '2023-11-11 12:28:55.272377');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (603, '123', 'Продажа #123', 3, '', 13, 1, '2023-11-11 12:28:55.284141');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (604, '122', 'Продажа #122', 3, '', 13, 1, '2023-11-11 12:28:55.294938');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (605, '121', 'Продажа #121', 3, '', 13, 1, '2023-11-11 12:28:55.305450');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (606, '120', 'Продажа #120', 3, '', 13, 1, '2023-11-11 12:28:55.316447');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (607, '119', 'Продажа #119', 3, '', 13, 1, '2023-11-11 12:28:55.326963');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (608, '118', 'Продажа #118', 3, '', 13, 1, '2023-11-11 12:28:55.338538');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (609, '117', 'Продажа #117', 3, '', 13, 1, '2023-11-11 12:28:55.350178');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (610, '116', 'Продажа #116', 3, '', 13, 1, '2023-11-11 12:28:55.362486');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (611, '115', 'Продажа #115', 3, '', 13, 1, '2023-11-11 12:28:55.372945');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (612, '114', 'Продажа #114', 3, '', 13, 1, '2023-11-11 12:28:55.384959');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (613, '113', 'Продажа #113', 3, '', 13, 1, '2023-11-11 12:28:55.396419');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (614, '112', 'Продажа #112', 3, '', 13, 1, '2023-11-11 12:28:55.408115');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (615, '111', 'Продажа #111', 3, '', 13, 1, '2023-11-11 12:28:55.419219');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (616, '110', 'Продажа #110', 3, '', 13, 1, '2023-11-11 12:28:55.430140');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (617, '109', 'Продажа #109', 3, '', 13, 1, '2023-11-11 12:28:55.440686');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (618, '108', 'Продажа #108', 3, '', 13, 1, '2023-11-11 12:28:55.452196');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (619, '107', 'Продажа #107', 3, '', 13, 1, '2023-11-11 12:28:55.463221');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (620, '106', 'Продажа #106', 3, '', 13, 1, '2023-11-11 12:28:55.474989');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (621, '105', 'Продажа #105', 3, '', 13, 1, '2023-11-11 12:28:55.485407');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (622, '104', 'Продажа #104', 3, '', 13, 1, '2023-11-11 12:28:55.497173');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (623, '103', 'Продажа #103', 3, '', 13, 1, '2023-11-11 12:28:55.508391');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (624, '102', 'Продажа #102', 3, '', 13, 1, '2023-11-11 12:28:55.517972');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (625, '101', 'Продажа #101', 3, '', 13, 1, '2023-11-11 12:28:55.529030');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (626, '100', 'Продажа #100', 3, '', 13, 1, '2023-11-11 12:28:55.539978');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (627, '99', 'Продажа #99', 3, '', 13, 1, '2023-11-11 12:28:55.551511');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (628, '98', 'Продажа #98', 3, '', 13, 1, '2023-11-11 12:28:55.563043');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (629, '97', 'Продажа #97', 3, '', 13, 1, '2023-11-11 12:28:55.574376');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (630, '2', 'Ната', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-11 16:07:08.050528');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (631, '27', 'Платье с вырезом из дайвинга миди', 2, '[{"changed": {"fields": ["\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f"]}}]', 7, 1, '2023-11-12 08:23:23.394272');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (632, '92', '447-красный-46-48', 2, '[]', 8, 1, '2023-11-12 10:26:26.333246');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (633, '5', 'Возврат #5', 3, '', 15, 1, '2023-11-12 15:17:00.063688');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (634, '4', 'Возврат #4', 3, '', 15, 1, '2023-11-12 15:17:00.074689');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (635, '3', 'Возврат #3', 3, '', 15, 1, '2023-11-12 15:17:00.085688');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (636, '7', 'Возврат #7', 3, '', 15, 1, '2023-11-12 15:26:03.686056');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (637, '6', 'Возврат #6', 3, '', 15, 1, '2023-11-12 15:26:03.702064');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (638, '191', 'Продажа #191', 3, '', 13, 1, '2023-11-12 17:12:13.471225');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (639, '190', 'Продажа #190', 3, '', 13, 1, '2023-11-12 17:12:13.485740');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (640, '189', 'Продажа #189', 3, '', 13, 1, '2023-11-12 17:12:13.496254');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (641, '188', 'Продажа #188', 3, '', 13, 1, '2023-11-12 17:12:13.507369');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (642, '187', 'Продажа #187', 3, '', 13, 1, '2023-11-12 17:12:13.517794');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (643, '186', 'Продажа #186', 3, '', 13, 1, '2023-11-12 17:12:13.528794');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (644, '185', 'Продажа #185', 3, '', 13, 1, '2023-11-12 17:12:13.538807');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (645, '184', 'Продажа #184', 3, '', 13, 1, '2023-11-12 17:12:13.551400');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (646, '183', 'Продажа #183', 3, '', 13, 1, '2023-11-12 17:12:13.563483');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (647, '182', 'Продажа #182', 3, '', 13, 1, '2023-11-12 17:12:13.573993');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (648, '181', 'Продажа #181', 3, '', 13, 1, '2023-11-12 17:12:13.585505');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (649, '180', 'Продажа #180', 3, '', 13, 1, '2023-11-12 17:12:13.596523');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (650, '179', 'Продажа #179', 3, '', 13, 1, '2023-11-12 17:12:13.608303');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (651, '178', 'Продажа #178', 3, '', 13, 1, '2023-11-12 17:12:13.621809');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (652, '177', 'Продажа #177', 3, '', 13, 1, '2023-11-12 17:12:13.632809');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (653, '176', 'Продажа #176', 3, '', 13, 1, '2023-11-12 17:12:13.643334');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (654, '175', 'Продажа #175', 3, '', 13, 1, '2023-11-12 17:12:13.654609');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (655, '174', 'Продажа #174', 3, '', 13, 1, '2023-11-12 17:12:13.664636');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (656, '173', 'Продажа #173', 3, '', 13, 1, '2023-11-12 17:12:13.674800');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (657, '172', 'Продажа #172', 3, '', 13, 1, '2023-11-12 17:12:13.685311');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (658, '171', 'Продажа #171', 3, '', 13, 1, '2023-11-12 17:12:13.695493');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (659, '170', 'Продажа #170', 3, '', 13, 1, '2023-11-12 17:12:13.706592');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (660, '169', 'Продажа #169', 3, '', 13, 1, '2023-11-12 17:12:13.716300');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (661, '168', 'Продажа #168', 3, '', 13, 1, '2023-11-12 17:12:13.726797');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (662, '167', 'Продажа #167', 3, '', 13, 1, '2023-11-12 17:12:13.737330');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (663, '166', 'Продажа #166', 3, '', 13, 1, '2023-11-12 17:12:13.747349');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (664, '165', 'Продажа #165', 3, '', 13, 1, '2023-11-12 17:12:13.757799');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (665, '164', 'Продажа #164', 3, '', 13, 1, '2023-11-12 17:12:13.768302');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (666, '163', 'Продажа #163', 3, '', 13, 1, '2023-11-12 17:12:13.778355');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (667, '162', 'Продажа #162', 3, '', 13, 1, '2023-11-12 17:12:13.789324');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (668, '161', 'Продажа #161', 3, '', 13, 1, '2023-11-12 17:12:13.799696');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (669, '160', 'Продажа #160', 3, '', 13, 1, '2023-11-12 17:12:13.810152');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (670, '159', 'Продажа #159', 3, '', 13, 1, '2023-11-12 17:12:13.820685');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (671, '158', 'Продажа #158', 3, '', 13, 1, '2023-11-12 17:12:13.830773');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (672, '157', 'Продажа #157', 3, '', 13, 1, '2023-11-12 17:12:13.841768');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (673, '156', 'Продажа #156', 3, '', 13, 1, '2023-11-12 17:12:13.852289');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (674, '9', 'Возврат #9', 3, '', 15, 1, '2023-11-12 17:12:24.889698');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (675, '8', 'Возврат #8', 3, '', 15, 1, '2023-11-12 17:12:24.901250');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (676, '9', 'Возврат #9', 3, '', 15, 1, '2023-11-12 17:14:13.414576');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (677, '10', 'Возврат #10', 3, '', 15, 1, '2023-11-12 17:14:17.982152');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (678, '8', 'Возврат #8', 3, '', 15, 1, '2023-11-12 17:14:21.031763');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (679, '194', 'Продажа #194', 3, '', 13, 1, '2023-11-12 17:14:40.925039');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (680, '193', 'Продажа #193', 3, '', 13, 1, '2023-11-12 17:14:40.937066');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (681, '192', 'Продажа #192', 3, '', 13, 1, '2023-11-12 17:14:40.947592');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (682, '8', 'Возврат #8', 3, '', 15, 1, '2023-11-12 17:14:47.231073');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (683, '51', '1026-мокко-42-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-54-10.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-54-07.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-54-04.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-54-02.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-53-59.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-53-56.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-53-53.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-53-50.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-53-48.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-53-38.jpg"}}]', 8, 1, '2023-11-15 19:55:27.159308');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (684, '85', '1002-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-24.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-21.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-18.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-15.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-13.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-11.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-09.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-06.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-56-00.jpg"}}]', 8, 1, '2023-11-15 19:56:55.478260');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (685, '84', '1002-черный-40-42', 2, '[]', 8, 1, '2023-11-15 19:57:00.906286');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (686, '55', '1029-черный-44-46', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-57-48.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-57-45.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-57-42.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-57-39.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-57-37.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-57-34.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-15_21-57-29.jpg"}}]', 8, 1, '2023-11-15 19:58:14.642524');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (687, '54', '1029-черный-40-42', 2, '[]', 8, 1, '2023-11-15 19:58:18.570290');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (688, '203', 'Продажа #203', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438 #236"}}]', 13, 1, '2023-11-15 19:59:46.503250');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (689, '1', 'Оприходование #1', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #1"}}]', 19, 1, '2023-11-16 07:57:07.637309');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (690, '2', 'Оприходование #2', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #2"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #3"}}]', 19, 1, '2023-11-16 07:58:26.406373');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (691, '2', 'Оприходование #2', 3, '', 19, 1, '2023-11-16 07:59:04.943682');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (692, '1', 'Оприходование #1', 3, '', 19, 1, '2023-11-16 07:59:04.952969');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (693, '3', 'Оприходование #3', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #4"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #5"}}]', 19, 1, '2023-11-16 07:59:20.691025');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (694, '3', 'Оприходование #3', 3, '', 19, 1, '2023-11-16 08:02:06.306823');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (695, '4', 'Оприходование #4', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #6"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #7"}}]', 19, 1, '2023-11-16 08:02:13.895234');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (696, '4', 'Оприходование #4', 3, '', 19, 1, '2023-11-16 08:11:56.898290');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (697, '5', 'Оприходование #5', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #8"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #9"}}]', 19, 1, '2023-11-16 08:12:21.006266');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (698, '5', 'Оприходование #5', 3, '', 19, 1, '2023-11-16 08:12:49.436511');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (699, '1', 'Списание товара #1', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430 #1"}}]', 21, 1, '2023-11-16 08:19:05.851861');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (700, '27', 'Платье с вырезом из дайвинга миди', 2, '[]', 7, 1, '2023-11-16 08:19:15.070846');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (701, '1', 'Списание товара #1', 3, '', 21, 1, '2023-11-16 08:19:48.510515');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (702, '2', 'Списание товара #2', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430 #2"}}]', 21, 1, '2023-11-16 08:29:45.256804');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (703, '6', 'Оприходование #6', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #10"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043e\u043f\u0440\u0438\u0445\u043e\u0434\u043e\u0432\u0430\u043d\u0438\u044f #11"}}]', 19, 1, '2023-11-16 08:44:31.333157');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (704, '3', 'Списание товара #3', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430 #3"}}]', 21, 1, '2023-11-16 08:44:55.188704');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (705, '27', 'Платье с вырезом из дайвинга миди', 2, '[]', 7, 1, '2023-11-16 08:45:02.948864');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (706, '16', 'Возврат #16', 1, '[{"added": {}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 #16"}}, {"added": {"name": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430", "object": "\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430 #17"}}]', 15, 1, '2023-11-16 08:49:05.358356');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (707, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 14:23:05.215086');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (708, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 14:30:38.953626');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (709, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 15:02:15.136958');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (710, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 15:48:18.239861');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (711, '1', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 15:48:28.866651');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (712, '1', 'Arg??', 3, '', 18, 1, '2023-11-16 15:52:23.609607');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (713, '3', 'Arg??', 3, '', 18, 1, '2023-11-16 15:57:03.814880');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (714, '4', 'Arg??', 3, '', 18, 1, '2023-11-16 16:07:21.541738');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (715, '5', 'Arg??', 3, '', 18, 1, '2023-11-16 16:10:09.753154');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (716, '6', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 16:11:31.700717');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (717, '6', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 16:11:50.880969');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (718, '6', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 16:12:14.968451');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (719, '6', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 16:12:27.739942');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (720, '6', 'Arg??', 2, '[]', 18, 1, '2023-11-16 16:13:27.518187');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (721, '6', 'Arg??', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 16:14:45.217242');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (722, '2', 'Ната', 2, '[{"changed": {"fields": ["\u0420\u043e\u043b\u044c"]}}]', 18, 1, '2023-11-16 17:00:34.170139');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (723, '6', 'Штаны', 1, '[{"added": {}}]', 9, 1, '2023-11-16 19:22:18.640555');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (724, '15', 'хаки', 1, '[{"added": {}}]', 11, 1, '2023-11-16 19:23:22.879088');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (725, '28', 'Штаны барашек', 1, '[{"added": {}}]', 7, 1, '2023-11-16 19:23:47.444271');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (726, '98', '1032-черный-48-52', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-24-10.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-23-55.jpg"}}]', 8, 1, '2023-11-16 19:24:29.294248');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (727, '96', '1032-хаки-48-52', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-24-15.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-24-08.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-23-55_SlplJcQ.jpg"}}]', 8, 1, '2023-11-16 19:24:49.196370');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (728, '94', '1032-беж-48-52', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-24-13.jpg"}}]', 8, 1, '2023-11-16 19:24:55.588917');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (729, '29', 'Платье прямое теплое', 1, '[{"added": {}}]', 7, 1, '2023-11-16 19:27:56.323888');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (730, '100', '1025-черный-46-48', 2, '[{"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-27-14.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-27-11.jpg"}}, {"added": {"name": "\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430", "object": "images/photo_2023-11-16_21-27-05.jpg"}}]', 8, 1, '2023-11-16 19:28:11.282064');

-- Таблица: django_content_type
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO django_content_type (id, app_label, model) VALUES (1, 'admin', 'logentry');
INSERT INTO django_content_type (id, app_label, model) VALUES (2, 'auth', 'permission');
INSERT INTO django_content_type (id, app_label, model) VALUES (3, 'auth', 'group');
INSERT INTO django_content_type (id, app_label, model) VALUES (4, 'auth', 'user');
INSERT INTO django_content_type (id, app_label, model) VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO django_content_type (id, app_label, model) VALUES (6, 'sessions', 'session');
INSERT INTO django_content_type (id, app_label, model) VALUES (7, 'catalog', 'product');
INSERT INTO django_content_type (id, app_label, model) VALUES (8, 'catalog', 'productmodification');
INSERT INTO django_content_type (id, app_label, model) VALUES (9, 'catalog', 'category');
INSERT INTO django_content_type (id, app_label, model) VALUES (10, 'catalog', 'image');
INSERT INTO django_content_type (id, app_label, model) VALUES (11, 'catalog', 'color');
INSERT INTO django_content_type (id, app_label, model) VALUES (12, 'catalog', 'size');
INSERT INTO django_content_type (id, app_label, model) VALUES (13, 'catalog', 'sale');
INSERT INTO django_content_type (id, app_label, model) VALUES (14, 'catalog', 'saleitem');
INSERT INTO django_content_type (id, app_label, model) VALUES (15, 'catalog', 'return');
INSERT INTO django_content_type (id, app_label, model) VALUES (16, 'catalog', 'returnitem');
INSERT INTO django_content_type (id, app_label, model) VALUES (17, 'catalog', 'stock');
INSERT INTO django_content_type (id, app_label, model) VALUES (18, 'catalog', 'telegramuser');
INSERT INTO django_content_type (id, app_label, model) VALUES (19, 'catalog', 'inventory');
INSERT INTO django_content_type (id, app_label, model) VALUES (20, 'catalog', 'inventoryitem');
INSERT INTO django_content_type (id, app_label, model) VALUES (21, 'catalog', 'writeoff');
INSERT INTO django_content_type (id, app_label, model) VALUES (22, 'catalog', 'writeoffitem');

-- Таблица: django_migrations
CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO django_migrations (id, app, name, applied) VALUES (1, 'contenttypes', '0001_initial', '2023-10-28 09:18:44.054208');
INSERT INTO django_migrations (id, app, name, applied) VALUES (2, 'auth', '0001_initial', '2023-10-28 09:18:44.086407');
INSERT INTO django_migrations (id, app, name, applied) VALUES (3, 'admin', '0001_initial', '2023-10-28 09:18:44.113428');
INSERT INTO django_migrations (id, app, name, applied) VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2023-10-28 09:18:44.129203');
INSERT INTO django_migrations (id, app, name, applied) VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2023-10-28 09:18:44.145537');
INSERT INTO django_migrations (id, app, name, applied) VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2023-10-28 09:18:44.166386');
INSERT INTO django_migrations (id, app, name, applied) VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2023-10-28 09:18:44.183351');
INSERT INTO django_migrations (id, app, name, applied) VALUES (8, 'auth', '0003_alter_user_email_max_length', '2023-10-28 09:18:44.201669');
INSERT INTO django_migrations (id, app, name, applied) VALUES (9, 'auth', '0004_alter_user_username_opts', '2023-10-28 09:18:44.216825');
INSERT INTO django_migrations (id, app, name, applied) VALUES (10, 'auth', '0005_alter_user_last_login_null', '2023-10-28 09:18:44.234346');
INSERT INTO django_migrations (id, app, name, applied) VALUES (11, 'auth', '0006_require_contenttypes_0002', '2023-10-28 09:18:44.249474');
INSERT INTO django_migrations (id, app, name, applied) VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2023-10-28 09:18:44.264494');
INSERT INTO django_migrations (id, app, name, applied) VALUES (13, 'auth', '0008_alter_user_username_max_length', '2023-10-28 09:18:44.282985');
INSERT INTO django_migrations (id, app, name, applied) VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2023-10-28 09:18:44.299611');
INSERT INTO django_migrations (id, app, name, applied) VALUES (15, 'auth', '0010_alter_group_name_max_length', '2023-10-28 09:18:44.317414');
INSERT INTO django_migrations (id, app, name, applied) VALUES (16, 'auth', '0011_update_proxy_permissions', '2023-10-28 09:18:44.331450');
INSERT INTO django_migrations (id, app, name, applied) VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2023-10-28 09:18:44.349124');
INSERT INTO django_migrations (id, app, name, applied) VALUES (18, 'catalog', '0001_initial', '2023-10-28 09:18:44.389579');
INSERT INTO django_migrations (id, app, name, applied) VALUES (19, 'sessions', '0001_initial', '2023-10-28 09:18:44.411594');
INSERT INTO django_migrations (id, app, name, applied) VALUES (20, 'catalog', '0002_rename_product_modification_image_modification', '2023-10-28 09:52:23.421399');
INSERT INTO django_migrations (id, app, name, applied) VALUES (21, 'catalog', '0003_image_processed_alter_category_slug_and_more', '2023-10-29 10:13:51.453800');
INSERT INTO django_migrations (id, app, name, applied) VALUES (22, 'catalog', '0004_remove_image_processed', '2023-10-29 10:15:12.938321');
INSERT INTO django_migrations (id, app, name, applied) VALUES (23, 'catalog', '0005_alter_productmodification_custom_sku', '2023-10-30 07:39:15.472377');
INSERT INTO django_migrations (id, app, name, applied) VALUES (24, 'catalog', '0006_alter_color_options_alter_size_options_and_more', '2023-10-30 19:12:46.627146');
INSERT INTO django_migrations (id, app, name, applied) VALUES (25, 'catalog', '0007_productmodification_slug_alter_category_slug_and_more', '2023-10-30 20:35:30.742242');
INSERT INTO django_migrations (id, app, name, applied) VALUES (26, 'catalog', '0008_productmodification_created_at_and_more', '2023-10-31 17:28:54.529460');
INSERT INTO django_migrations (id, app, name, applied) VALUES (27, 'catalog', '0009_sale_saleitem_sale_products', '2023-10-31 18:07:22.889018');
INSERT INTO django_migrations (id, app, name, applied) VALUES (28, 'catalog', '0009_sale_saleitem', '2023-10-31 18:17:18.229705');
INSERT INTO django_migrations (id, app, name, applied) VALUES (29, 'catalog', '0009_sale', '2023-10-31 18:38:02.554949');
INSERT INTO django_migrations (id, app, name, applied) VALUES (30, 'catalog', '0010_delete_sale', '2023-10-31 19:04:34.196566');
INSERT INTO django_migrations (id, app, name, applied) VALUES (31, 'catalog', '0011_sale_saleitem', '2023-11-01 19:00:46.441097');
INSERT INTO django_migrations (id, app, name, applied) VALUES (32, 'catalog', '0012_remove_sale_products_sale_modifications_and_more', '2023-11-02 17:46:09.992432');
INSERT INTO django_migrations (id, app, name, applied) VALUES (33, 'catalog', '0013_remove_sale_modifications_remove_sale_quantity_and_more', '2023-11-02 18:05:52.611395');
INSERT INTO django_migrations (id, app, name, applied) VALUES (34, 'catalog', '0014_remove_sale_total_amount', '2023-11-02 18:09:05.199171');
INSERT INTO django_migrations (id, app, name, applied) VALUES (35, 'catalog', '0015_remove_saleitem_unit_price', '2023-11-02 18:10:37.230262');
INSERT INTO django_migrations (id, app, name, applied) VALUES (36, 'catalog', '0016_sale_comment_sale_payment_method_sale_status_and_more', '2023-11-02 18:53:57.395147');
INSERT INTO django_migrations (id, app, name, applied) VALUES (37, 'catalog', '0017_sale_source', '2023-11-02 19:03:12.053354');
INSERT INTO django_migrations (id, app, name, applied) VALUES (38, 'catalog', '0018_productmodification_sold_count', '2023-11-05 12:09:20.376079');
INSERT INTO django_migrations (id, app, name, applied) VALUES (39, 'catalog', '0019_remove_productmodification_sold_count', '2023-11-05 12:20:11.551883');
INSERT INTO django_migrations (id, app, name, applied) VALUES (40, 'catalog', '0020_return_alter_sale_created_at_alter_saleitem_quantity_and_more', '2023-11-06 11:03:46.063519');
INSERT INTO django_migrations (id, app, name, applied) VALUES (41, 'catalog', '0021_stock', '2023-11-06 12:34:11.262905');
INSERT INTO django_migrations (id, app, name, applied) VALUES (42, 'catalog', '0022_delete_stock', '2023-11-06 12:34:43.084679');
INSERT INTO django_migrations (id, app, name, applied) VALUES (43, 'catalog', '0023_telegramuser', '2023-11-09 17:41:41.882724');
INSERT INTO django_migrations (id, app, name, applied) VALUES (44, 'catalog', '0024_alter_telegramuser_options_return_telegram_user_and_more', '2023-11-09 19:58:23.457323');
INSERT INTO django_migrations (id, app, name, applied) VALUES (45, 'catalog', '0025_inventory_inventoryitem', '2023-11-16 07:54:20.523889');
INSERT INTO django_migrations (id, app, name, applied) VALUES (46, 'catalog', '0026_alter_inventoryitem_inventory', '2023-11-16 07:56:55.157405');
INSERT INTO django_migrations (id, app, name, applied) VALUES (47, 'catalog', '0027_writeoff_alter_inventoryitem_quantity_writeoffitem', '2023-11-16 08:18:43.674870');
INSERT INTO django_migrations (id, app, name, applied) VALUES (48, 'catalog', '0028_rename_username_telegramuser_user_name', '2023-11-16 16:06:42.401136');

-- Таблица: django_session
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('w8oadspftzrx9yosfoqo3bx0xk5uwmp9', '.eJxVjMsOwiAQRf-FtSGUxwAu3fsNZBimUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnMYjT75aRHtx2UO7YbrOkua3LlOWuyIN2eZ0LPy-H-3dQsddvrZ0LDhx5Q4qxgFEQ2QGCNwikNXAgCmZkH4phW5TPo3UYPQ4qWu3F-wPMOTdV:1qwfxl:Xl3N2QaNOiLc9_dRlQretuxvTE9DZzXyzcrQYJ8QfWg', '2023-11-11 09:50:37.766813');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('1hx3yi9troeauwnt0fatzijl57u4qivp', '.eJxVjMsOwiAQRf-FtSGUxwAu3fsNZBimUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnMYjT75aRHtx2UO7YbrOkua3LlOWuyIN2eZ0LPy-H-3dQsddvrZ0LDhx5Q4qxgFEQ2QGCNwikNXAgCmZkH4phW5TPo3UYPQ4qWu3F-wPMOTdV:1r1kmD:a72BRnpOzySA0_SXuz5ycL5qEKDs20auh7xbZICwFUA', '2023-11-25 09:59:41.923789');

-- Индекс: auth_group_permissions_group_id_b120cbf9
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

-- Индекс: auth_group_permissions_group_id_permission_id_0cd325b0_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

-- Индекс: auth_group_permissions_permission_id_84c5c92e
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

-- Индекс: auth_permission_content_type_id_2f476e4b
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

-- Индекс: auth_permission_content_type_id_codename_01ab375a_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

-- Индекс: auth_user_groups_group_id_97559544
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");

-- Индекс: auth_user_groups_user_id_6a12ed8b
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");

-- Индекс: auth_user_groups_user_id_group_id_94350c0c_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");

-- Индекс: auth_user_user_permissions_permission_id_1fbb5f2c
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");

-- Индекс: auth_user_user_permissions_user_id_a95ead1b
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");

-- Индекс: auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");

-- Индекс: catalog_image_modification_id_8bfc7cad
CREATE INDEX IF NOT EXISTS "catalog_image_modification_id_8bfc7cad" ON "catalog_image" ("modification_id");

-- Индекс: catalog_inventory_telegram_user_id_9b7dd549
CREATE INDEX IF NOT EXISTS "catalog_inventory_telegram_user_id_9b7dd549" ON "catalog_inventory" ("telegram_user_id");

-- Индекс: catalog_inventory_user_id_4da38d68
CREATE INDEX IF NOT EXISTS "catalog_inventory_user_id_4da38d68" ON "catalog_inventory" ("user_id");

-- Индекс: catalog_inventoryitem_inventory_id_03397e86
CREATE INDEX IF NOT EXISTS "catalog_inventoryitem_inventory_id_03397e86" ON "catalog_inventoryitem" ("inventory_id");

-- Индекс: catalog_inventoryitem_product_modification_id_bde6a6ed
CREATE INDEX IF NOT EXISTS "catalog_inventoryitem_product_modification_id_bde6a6ed" ON "catalog_inventoryitem" ("product_modification_id");

-- Индекс: catalog_product_category_id_35bf920b
CREATE INDEX IF NOT EXISTS "catalog_product_category_id_35bf920b" ON "catalog_product" ("category_id");

-- Индекс: catalog_product_colors_color_id_e339a19f
CREATE INDEX IF NOT EXISTS "catalog_product_colors_color_id_e339a19f" ON "catalog_product_colors" ("color_id");

-- Индекс: catalog_product_colors_product_id_70525b5f
CREATE INDEX IF NOT EXISTS "catalog_product_colors_product_id_70525b5f" ON "catalog_product_colors" ("product_id");

-- Индекс: catalog_product_colors_product_id_color_id_1b754e02_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "catalog_product_colors_product_id_color_id_1b754e02_uniq" ON "catalog_product_colors" ("product_id", "color_id");

-- Индекс: catalog_product_sizes_product_id_7f0e6f5f
CREATE INDEX IF NOT EXISTS "catalog_product_sizes_product_id_7f0e6f5f" ON "catalog_product_sizes" ("product_id");

-- Индекс: catalog_product_sizes_product_id_size_id_fea46a07_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "catalog_product_sizes_product_id_size_id_fea46a07_uniq" ON "catalog_product_sizes" ("product_id", "size_id");

-- Индекс: catalog_product_sizes_size_id_f5ee90f1
CREATE INDEX IF NOT EXISTS "catalog_product_sizes_size_id_f5ee90f1" ON "catalog_product_sizes" ("size_id");

-- Индекс: catalog_productmodification_color_id_9ac59ef3
CREATE INDEX IF NOT EXISTS "catalog_productmodification_color_id_9ac59ef3" ON "catalog_productmodification" ("color_id");

-- Индекс: catalog_productmodification_product_id_a278c6f5
CREATE INDEX IF NOT EXISTS "catalog_productmodification_product_id_a278c6f5" ON "catalog_productmodification" ("product_id");

-- Индекс: catalog_productmodification_product_id_color_id_size_id_cb4af358_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "catalog_productmodification_product_id_color_id_size_id_cb4af358_uniq" ON "catalog_productmodification" ("product_id", "color_id", "size_id");

-- Индекс: catalog_productmodification_size_id_2f87f850
CREATE INDEX IF NOT EXISTS "catalog_productmodification_size_id_2f87f850" ON "catalog_productmodification" ("size_id");

-- Индекс: catalog_productmodification_slug_b76e9b8c
CREATE INDEX IF NOT EXISTS "catalog_productmodification_slug_b76e9b8c" ON "catalog_productmodification" ("slug");

-- Индекс: catalog_return_telegram_user_id_4c11669c
CREATE INDEX IF NOT EXISTS "catalog_return_telegram_user_id_4c11669c" ON "catalog_return" ("telegram_user_id");

-- Индекс: catalog_return_user_id_91fc13d6
CREATE INDEX IF NOT EXISTS "catalog_return_user_id_91fc13d6" ON "catalog_return" ("user_id");

-- Индекс: catalog_returnitem_product_modification_id_ff9da4b5
CREATE INDEX IF NOT EXISTS "catalog_returnitem_product_modification_id_ff9da4b5" ON "catalog_returnitem" ("product_modification_id");

-- Индекс: catalog_returnitem_return_sale_id_09013a4f
CREATE INDEX IF NOT EXISTS "catalog_returnitem_return_sale_id_09013a4f" ON "catalog_returnitem" ("return_sale_id");

-- Индекс: catalog_sale_telegram_user_id_13083842
CREATE INDEX IF NOT EXISTS "catalog_sale_telegram_user_id_13083842" ON "catalog_sale" ("telegram_user_id");

-- Индекс: catalog_sale_user_id_25fdf1a4
CREATE INDEX IF NOT EXISTS "catalog_sale_user_id_25fdf1a4" ON "catalog_sale" ("user_id");

-- Индекс: catalog_saleitem_product_modification_id_d159d59a
CREATE INDEX IF NOT EXISTS "catalog_saleitem_product_modification_id_d159d59a" ON "catalog_saleitem" ("product_modification_id");

-- Индекс: catalog_saleitem_sale_id_4cee86a4
CREATE INDEX IF NOT EXISTS "catalog_saleitem_sale_id_4cee86a4" ON "catalog_saleitem" ("sale_id");

-- Индекс: catalog_writeoff_telegram_user_id_af751a10
CREATE INDEX IF NOT EXISTS "catalog_writeoff_telegram_user_id_af751a10" ON "catalog_writeoff" ("telegram_user_id");

-- Индекс: catalog_writeoff_user_id_0cfda9a1
CREATE INDEX IF NOT EXISTS "catalog_writeoff_user_id_0cfda9a1" ON "catalog_writeoff" ("user_id");

-- Индекс: catalog_writeoffitem_product_modification_id_1aeca645
CREATE INDEX IF NOT EXISTS "catalog_writeoffitem_product_modification_id_1aeca645" ON "catalog_writeoffitem" ("product_modification_id");

-- Индекс: catalog_writeoffitem_write_off_id_b75dd22b
CREATE INDEX IF NOT EXISTS "catalog_writeoffitem_write_off_id_b75dd22b" ON "catalog_writeoffitem" ("write_off_id");

-- Индекс: django_admin_log_content_type_id_c4bce8eb
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

-- Индекс: django_admin_log_user_id_c564eba6
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

-- Индекс: django_content_type_app_label_model_76bd3d3b_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

-- Индекс: django_session_expire_date_a5c62663
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
