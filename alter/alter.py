""" 
if chapter number is the same add value on the subchapter
"""

"""
WITH RankedChapters AS (
    SELECT c.chapter_id,
           ROW_NUMBER() OVER (PARTITION BY c.novel_id, c.index ORDER BY c.timestamp) AS subchapter
    FROM chapters c
    WHERE EXISTS (
        SELECT 1
        FROM chapters c2
        WHERE c2.novel_id = c.novel_id AND c2.index = c.index
        HAVING COUNT(*) > 1
    )
)
UPDATE chapters c
SET subchapter = rc.subchapter
FROM RankedChapters rc
WHERE c.chapter_id = rc.chapter_id;
"""

""" 
query all chapter with dups numbers as it has subchapter
"""
"""
SELECT c.*
FROM chapters c
JOIN (
    SELECT novel_id, index
    FROM chapters
    GROUP BY novel_id, index
    HAVING COUNT(*) > 1
) dup ON c.novel_id = dup.novel_id AND c.index = dup.index;
 """

""" check of novel endchapter and latest novel chapter index is matched """
"""
        SELECT n.last_chapter, c.index, c.title, c.timestamp AS last_timestamp
        FROM novels n
        JOIN chapters c ON n.novel_id = c.novel_id
        WHERE n.novel_id = 143
        ORDER BY c.timestamp DESC
        LIMIT 1;

    UPDATE novels SET last_chapter = 1134 WHERE novel_id = 141;
"""