show grants
```mysql
SHOW GRANTS FOR '$USERNAME';
```

create temporary storage
```mysql
GRANT CREATE TEMPORARY TABLES ON `$SCHEMA`.$ TO `DB_NAME`@`%`;
```

truncate table
```mysql
DELETE FROM $TABLE WHERE $FIELD = $VALUE;
```
