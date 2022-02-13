SELECT * FROM auth_user

DELETE FROM rareapi_post WHERE id>1

UPDATE auth_user
SET is_staff = 0
WHERE id=1;