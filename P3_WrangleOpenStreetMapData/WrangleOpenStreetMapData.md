
_________________________________________________________________________________________________________________
# Project: OpenStreetMap Data Wrangling 
__________________________________________________________________________________________________________________

### Map Area : Singapore

- https://mapzen.com/data/metro-extracts/metro/singapore/  
 This map is the area of Singapore. I would like to explore this extract a little bit and see what interesting data I can find.  
 
 
 

## Problems Encountered in the Map
__________________________________________________________________________________________________________________
- ### Inconsistent Street Name

After downloading a sample of my OSM dataset, I started the wrangling process by investigating the various elements for this project. The initial audit revealed some inconsistencies in the street type addresses (`audit_street` in `audit_street.py`). There were several street names with its kind abbreviated (`"Woodlands Ave 9", "Bah Soon Pah Rd"`) or contain block numbers/house numbers (`"Jalan Rajah, #01-01, Zhong Shan Park", "41 lorong 16 geylang"`).  

To deal with above problems, I created a map to convert abbreviations to complete street types (see `mapping` in `audit_street.py`). I also cleaned block numbers/house numbers and capitalized in street names.  
The code I used for standardizing the street name data(in file `audit_street.py`) is shown below:  
```python
    def update_type(street_name):
        try:
            street_type = street_type_re.search(street_name).group()
            return street_name.replace(street_type, mapping[street_type])
        except:
            return street_name

    def clean_redundant(street_name):
        street_name = re.sub(number_house_re, '', street_name)
        return re.sub(area_re, '', street_name).title().replace('\n', '')

    def update_street_name(street_name):
        return update_type(clean_redundant(street_name))
```  
After the update, we solved the abbreviation problem was for almost all cases, excluding only stranger ones probably caused by erroneous human inputs.  

- ### Inconsistent Amenity
Another problem that I noticed while parsing through the data was that the inconsistent amenity tags (using method `audit_amenity` in `audit_amenity.py`).  
I also present bits of the code that I used to tackle with them (the code that follows is part of `audit_amenities.py`).  

```python
    mapping = {
        'carpark': 'parking',
        'coffeeshop': 'cafe',
        'internet cafe': 'cafe',
        'deli': 'food_court',
        'Mail drop': 'post_box',
        'childcare': 'childcare_centre',
        'bar;restaurant': 'bar',
        'restaurant;taxi': 'taxi'
    }

    def update_amenity(amenity):
        return mapping.get(amenity, amenity).lower().replace(' ', '_')

```

## Data Overview
__________________________________________________________________________________________________________________
This section contains basic statistics about the dataset and the SQL queries used to collect the data.  
- ### File sizes
```
    singapore.osm ......... 341.5 MB
    singapore.db .......... 238.6 MB
    nodes.csv ............. 123.2 MB
    nodes_tags.csv ........   5.0 MB
    ways.csv ..............  14.1 MB
    ways_tags.csv .........  22.2 MB
    ways_nodes.cv .........  45.1 MB  
```  

- ### Number of nodes
```sql
sqlite> SELECT COUNT(*) FROM nodes;
```  
```sql 
    +--------+
    |1503062 |
    +--------+```

- ### Number of nodes
```sql
sqlite> SELECT COUNT(*) FROM ways;```
```sql 
    +--------+
    | 235828 |
    +--------+```

- ### Number of unique users
```sql    
sqlite> SELECT COUNT(DISTINCT(e.uid)) 
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;```
```sql
    +--------+
    |  2103  |
    +--------+ ```
    
- ### Top 10 contributing users
```sql 
sqlite> SELECT e.user , COUNT(*) as count
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY count DESC
LIMIT 10;```
```sql 
    +-------------------------------+--------+
    | User                          | Total  |
    +-------------------------------+--------+
    | JaLooNz                       | 400100 |
    | berjaya                       | 117571 |
    | rene78                        | 77843  |
    | cboothroyd                    | 72535  |
    | lmum                          | 44058  |
    | kingrollo                     | 39164  |
    | Luis36995                     | 38830  |
    | ridixcr                       | 38256  |
    | Sihabul Milah                 | 37189  |
    | calfarome                     | 32946  |
    +-------------------------------+--------+ ```

- ### Number of users appearing only onces
```sql 
sqlite> SELECT COUNT(*) 
FROM(
    SELECT e.user, COUNT(*) as num
    FROM (
        SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1)```
```sql
    +--------+
    |  594   |
    +--------+```
    
- ### Most popular keys of tag
```sql 
sqlite> SELECT t.key , COUNT(*) as Total
FROM (SELECT key FROM nodes_tags UNION ALL SELECT key FROM ways_tags) t
GROUP BY t.key
ORDER BY Total DESC
LIMIT 10;```
```sql 
    +-------------------------------+--------+
    | Key                           | Total  |
    +-------------------------------+--------+
    | building                      | 120636 |
    | highway                       | 102327 |
    | name                          | 77246  |
    | source                        | 55350  |
    | street                        | 43058  |
    | surface                       | 32039  |
    | city                          | 30840  |
    | housenumber                   | 29768  |
    | oneway                        | 27344  |
    | lanes                         | 22589  |
    +-------------------------------+--------+ ```


## Additional Data Exploration 
_________________________________________________________________________________________________________________
- ### Top 10 Amenity Types
```sql
sqlite> SELECT value as Amenity, COUNT(DISTINCT(id)) as Total
FROM nodes_tags 
WHERE key='amenity'
GROUP BY value
ORDER BY Total DESC 
LIMIT 10;```
```sql
    +-------------------------------+--------+
    | Amenity                       | Total  |
    +-------------------------------+--------+
    | restaurant                    | 2149   |
    | atm                           | 823    |
    | place_of_worship              | 587    |
    | cafe                          | 545    |
    | parking                       | 532    |
    | fast_food                     | 409    |
    | taxi                          | 335    |
    | bank                          | 325    |
    | toilets                       | 226    |
    | shelter                       | 208    |
    +-------------------------------+--------+
```
        
- ### Top 10 Fast food restaurant with the most branches
```sql
sqlite> SELECT nodes_tags.value as Name, COUNT(*) as Total
FROM nodes_tags
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='fast_food') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='name'
GROUP BY nodes_tags.value
ORDER BY Total DESC
LIMIT 10;```
```sql
    +-------------------------------+--------+
    | Name                          | Total  |
    +-------------------------------+--------+
    | McDonald's                    | 90     |
    | KFC                           | 67     |
    | Subway                        | 33     |
    | Burger King                   | 23     |
    | Domino's Pizza                | 8      |
    | Pizza Hut                     | 8      |
    | Long John Silver's            | 6      |
    | McDonalds                     | 5      |
    | Mcdonald's                    | 4      |
    | Mos Burger                    | 4      |
    +-------------------------------+--------+
``` 
We can see a quite bit of dirty data from the above query. For instance, there are at least three diversity names for `McDonald's`.  

- ### Top 10 Coffee shop with the most branches
```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as Total
FROM nodes_tags
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='cafe') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='name'
GROUP BY nodes_tags.value
ORDER BY Total DESC
LIMIT 10;```
```sql
+-------------------------------+--------+
| Name                          | Total  |
+-------------------------------+--------+
| Starbucks                     | 57     |
| The Coffee Bean & Tea Leaf    | 13     |
| Toast Box                     | 8      |
| Starbucks Coffee              | 6      |
| Coffee Bean & Tea Leaf        | 4      |
| Coffee Shop                   | 4      |
| The Coffee Bean and Tea Leaf  | 4      |
| Killiney Kopitiam             | 3      |
| Koi Cafe                      | 3      |
| Lola's Cafe                   | 3      |
+-------------------------------+--------+ 
```
The same issue comes in with Coffee shop, at least two names for `"Starbucks"` and three names for `"The Coffee Bean & Tea Leaf"`.  

- ### Top 5 Shop Types
```sql
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags 
WHERE key='shop'
GROUP BY value
ORDER BY num DESC 
LIMIT 5;```
```sql
    +-------------------------------+--------+
    | Shop                          | Total  |
    +-------------------------------+--------+
    | yes                           | 661    |
    | supermarket                   | 319    |
    | convenience                   | 304    |
    | clothes                       | 124    |
    | beauty                        | 122    |
    +-------------------------------+--------+```

- ### Top 10 Convenience shop with the most branches
```sql
SELECT nodes_tags.value AS NAME, COUNT(*) as Total
FROM nodes_tags
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='convenience') i
    ON nodes_tags.id=i.id
    WHERE nodes_tags.key='name'
GROUP BY nodes_tags.value
ORDER BY Total DESC
LIMIT 10;```
```sql
    +-------------------------------+--------+
    | Name                          | Total  |
    +-------------------------------+--------+
    | 7-Eleven                      | 105    |
    | Cheers                        | 22     |
    | 7 eleven                      | 17     |
    | 7 Eleven                      | 9      |
    | 7-eleven                      | 6      |
    | 7-11                          | 4      |
    | Mini Market                   | 4      |
    | I-Tec Supermart               | 3      |
    | 7/11                          | 2      |
    | 7Eleven                       | 2      |
    +-------------------------------+--------+```
Here we can notice that 7-Eleven has the most locations. Moreover, this chain of convenience shop occupied 7 positions of 10 first ranks with different names.  

- ### Total MRT/LRT stations
```sql 
SELECT COUNT(DISTINCT(nodes_tags.value)) as total
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE key='station') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='name'```
```sql
    +--------+
    |  130   |
    +--------+```

- ### Top 5 Religions
```sql
sqlite> SELECT nodes_tags.value as Religion, COUNT(*) as Total
FROM nodes_tags
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
    WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY Total DESC
LIMIT 5;```
```sql
    +-------------------------------+--------+
    | Religion                      | Total  |
    +-------------------------------+--------+
    | muslim                        | 414    |
    | christian                     | 83     |
    | buddhist                      | 25     |
    | hindu                         | 5      |
    | jewish                        | 3      |
    +-------------------------------+--------+```
    
- ###  The percentage of the given postcode for most popular Amenity, Shop, Tourism Types 
```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as Total, 1.00 * COUNT([pkey])/COUNT(*) as Percentage
FROM nodes_tags
    LEFT JOIN (SELECT DISTINCT(id), key as pkey FROM nodes_tags WHERE key='postcode') as i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='amenity' or nodes_tags.key='tourism' or nodes_tags.key='shop'
GROUP BY nodes_tags.value 
ORDER BY Total DESC 
LIMIT 20;```
```sql
    +-------------------------------+--------+---------------+
    | Value                         | Total  | Percentage(%) |
    +-------------------------------+--------+---------------+
    | restaurant                    | 2149   | 20            |
    | atm                           | 823    | 71            |
    | yes                           | 667    | 0             |
    | place_of_worship              | 587    | 2             |
    | cafe                          | 545    | 24            |
    | parking                       | 532    | 0             |
    | hotel                         | 441    | 74            |
    | fast_food                     | 409    | 9             |
    | taxi                          | 335    | 0             |
    | bank                          | 325    | 32            |
    | supermarket                   | 319    | 13            |
    | convenience                   | 304    | 6             |
    | attraction                    | 239    | 11            |
    | toilets                       | 226    | 0             |
    | shelter                       | 208    | 0             |
    | school                        | 179    | 12            |
    | fuel                          | 164    | 4             |
    | bar                           | 156    | 23            |
    | police                        | 141    | 5             |
    | food_court                    | 137    | 7             |
    +-------------------------------+--------+---------------+```


## Additional Ideas
_________________________________________________________________________________________________________________

- Cleaning the dirty data (diversity names of the cafe, fast food restaurant, convenience shop) mentioned in the additional exploration section would make our queries more accurate.
- The percentage of the given postcode for most popular amenity, shop, tourism types are quite low. We can add the postal code for these place will provide extra value in the open street map. If the address is dirty or missing, we can get it from the postal code in Singapore mostly. 
