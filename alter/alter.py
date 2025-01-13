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