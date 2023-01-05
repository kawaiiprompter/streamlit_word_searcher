import numpy as np
import pandas as pd
import streamlit as st

footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
height: 25px;
width: 100%;
font_size="0.8rem";
background-color: grey;
color: lightgrey;
text-align: center;
z-index: 100;
}
</style>
<div class="footer">
<p>Developed by <a href="https://twitter.com/kawaiiprompter" target="_blank">chili@kawaiiprompter</a></p>
</div>
"""

def load_csv(filename):
    datas = []
    with open(filename, "r") as fp:
        for line in fp:
            datas.append(line.strip())
    return datas


@st.cache()
def load_cache():
    movements = load_csv("data/movements.txt")
    mediums = load_csv("data/mediums.txt")
    flavors = load_csv("data/flavors.txt")
    
    danbooru_tags_all = pd.read_csv("data/wd14_selected_tags.csv")
    danbooru_tags = danbooru_tags_all.iloc[4:][["name", "count"]]
    
    return movements, mediums, flavors, danbooru_tags


def search(search_word, word_list):
    results = []
    for w in word_list:
        if search_word in w:
            results.append(w)
    return results


def main():
    st.set_page_config(page_title="Word Searcher")
    st.markdown(footer, unsafe_allow_html=True)
    
    st.markdown("## search word in wd14-tagger & CLIP Interrogator")
    movements, mediums, flavors, danbooru_tags = load_cache()
    search_word = st.text_input("検索ワード")
    max_size = st.selectbox("表示最大数", [20, 100, 200, 500, 1000])

    labels = [
        "flavors",
        "mediums (an illustration ofなど)",
        "movements (abstract artなど)",
    ]
    v_lists = [
        flavors,
        mediums,
        movements,
    ]
    
    if search_word != "":
        # WD14
        pick_tags = danbooru_tags[danbooru_tags["name"].map(lambda x: search_word in x)]
        st.markdown(f"### wd14-tagger")
        if len(pick_tags) == 0:
            st.text("search results: 0")
        else:
            st.text(f"search results: {len(pick_tags)}")
            st.dataframe(
                pick_tags.iloc[:max_size],
                300
            )
        
        # CLIP Interrogator
        for label, word_list in zip(labels, v_lists):
            st.markdown(f"### {label}")
            pick_word_list = search(search_word, word_list)
            if len(pick_word_list) == 0:
                st.text("search results: 0")
            else:
                st.text(f"search results: {len(pick_word_list)}")
                st.dataframe(
                    pd.DataFrame(np.array(pick_word_list[:max_size])),
                    300
                )


if __name__ == "__main__":
    main()