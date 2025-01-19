-- SCRIPT 'tabla1'

INSERT INTO as.tabla1 (id, nombre, descripcion) VALUES (1, 'producto1', 'descripcion1');
INSERT INTO as.tabla1 (id, nombre, descripcion) VALUES (2, SYSDATE, 'descripcion2');

-- SCRIPT 'tabla2'

INSERT INTO as.tabla2 (id, id_tabla1, detalle) VALUES (1, NULL, TO_DATE('1998-02-15', 'YYYY-MM-DD'));
INSERT INTO as.tabla2 (id, id_tabla1, detalle) VALUES (2, 0.0, TO_DATE('1998-02-16', 'YYYY-MM-DD'));


-- ROLLBACK 'tabla1'
DELETE FROM as.tabla1 WHERE id = 1 AND nombre = 'producto1' AND descripcion = 'descripcion1';
DELETE FROM as.tabla1 WHERE id = 2 AND nombre = SYSDATE AND descripcion = 'descripcion2';

-- ROLLBACK 'tabla2'
DELETE FROM as.tabla2 WHERE id = 1 AND id_tabla1 = NULL AND detalle = TO_DATE('1998-02-15', 'YYYY-MM-DD');
DELETE FROM as.tabla2 WHERE id = 2 AND id_tabla1 = 0.0 AND detalle = TO_DATE('1998-02-16', 'YYYY-MM-DD');
