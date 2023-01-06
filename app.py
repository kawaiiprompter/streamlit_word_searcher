import numpy as np
import pandas as pd
import streamlit as st

from footer import footer

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


def search(search_words, word_list):
    results = []
    for w in word_list:
        if all([
            search_word in w
            for search_word in search_words.split(" ")
            ]):
            results.append(w)
    return results


def main():
    st.set_page_config(page_title="Word Searcher")
    st.markdown(footer, unsafe_allow_html=True)
    
    st.markdown("## Finding word from wd14-tagger & CLIP Interrogator")
    movements, mediums, flavors, danbooru_tags = load_cache()
    search_words = st.text_input("検索ワード").lower()
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
    
    if search_words != "":
        # WD14
        def map_search(target_word):
            flg_exist_list = [
                search_word in target_word
                for search_word in search_words.split(" ")
            ]
            return all(flg_exist_list)
        pick_tags = danbooru_tags[danbooru_tags["name"].map(map_search)]
        st.markdown("### wd14-tagger")
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
            pick_word_list = search(search_words, word_list)
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