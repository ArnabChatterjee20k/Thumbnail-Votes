CREATE TABLE voters (
    user_id VARCHAR(40) NOT NULL,
    thumbnail_voted INTEGER NOT NULL,
    CONSTRAINT pk_id PRIMARY KEY (user_id, thumbnail_voted),
    FOREIGN KEY (thumbnail_voted) REFERENCES vote (thumbnail_id)
);