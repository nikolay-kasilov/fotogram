# Описание

## Модели
1. Users
   1. fullname
   2. username
   3. password (hash)
   4. birthday (nullable)
   5. bio
   6. signup_at (не принимается а заполняется текщим временем)
   7. last_action (автообновление после каждого действия)
   8. avatar (строка обозначающая путь в файловой системе) 

2. Posts
   1. photo
   2. content
   3. created_at
   4. author_id

3. Likes_Posts
   1. post_id
   2. user_id

4. Comments
   1. post_id
   2. comment_parent_id
   3. user_id
   4. content

5. Subscribes
   1. author_id
   2. subscriber_id