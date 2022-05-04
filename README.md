# <p style="text-align: center;"> Spotify & Productivity <p>

This GitHub repository holds the code for the final prototype for the course 02808 Personal Data Interaction for Mobile and Wearables, taught from February 2nd. 2022 to May 11th. 2022 at the Technical University of Denmark (DTU), Lyngby, Copenhagen.


### General Information:
- **DTU Course**: [02808 Personal Data Interaction for Mobile and Wearables](https://kurser.dtu.dk/course/02808)


- **Course timeline**: February 2nd., 2022 - May 11th., 2022


- **Project deadline**: May 11th., 2022


- **Creators & Contributors**:
    - [Christian Røssel](https://github.com/ChristianRoessel), Human Centered Artificial Intelligence, Technical University of Denmark (DTU), Copenhagen, Denmark, s213554@dtu.dk
    - [Chrysostomos Papadopoulos](https://github.com/Chrypapado), Human Centered Artificial Intelligence, Technical University of Denmark (DTU), Copenhagen, Denmark, s210603@dtu.dk
    - [Charidimos Vradis](https://github.com/haridimos9), Human Centered Artificial Intelligence, Technical University of Denmark (DTU), Copenhagen, Denmark, s212441@dtu.dk


### Final paper
See the scientific paper (final project):
- **[Overleaf Project (Scientific Paper)](https://www.overleaf.com/read/zfbkwsnfyknj)**

### Final prototype
She the application (running and hosted on Streamlit framework and servers), click the following link:
- [**View the prototype**](https://share.streamlit.io/haridimos9/final_project/main/app.py)


---




For privacy reasons, the **Client ID** and **Client Secret** *has been removed* in the following .py and .ipynb files (GitHub path): <br>

- `spotify_enrich_MyData` &#8594; `1_spotify_enrichment.ipynb`
- `spotify_get_data` &#8594; `get_data` &#8594; `server.py`

    
---
    
    
### To be able to run this app yourself:
1. [Create a Spotify developer account](https://developer.spotify.com/)
2. [Create s Spotify application](https://developer.spotify.com/dashboard/applications/)
3. Find your Client ID and Client Secret in your [Spotify developer dashboard](https://developer.spotify.com/dashboard/).
4. Add **Client ID** and **Client Secret** to (`INSERT_CLIENT_ID` & `INSERT_CLIENT_SECTRET`) in the following files:
- `spotify_enrich_MyData` &#8594; `1_spotify_enrichment.ipynb` and 
- `spotify_get_data` &#8594; `get_data` &#8594; `server.py`


---

### Extra info:
For `spotify_enrich_MyData` &#8594;
- `1_spotify_enrichment.ipynb`, 
- `2_activity_enrichment.ipynb` and 
- `3_spotify_visualisations.ipynb` 

$\ldots$ to work, you will need to have some data available. Example data for this application to work can be found in the following path
- `spotify_enrich_MyData` &#8594; `MyData` &#8594; `StreamingHistory3.json`
