import streamlit as st
import json
import os
from PyPDF2 import PdfReader
from google import genai


# ==========================
# ページ初期設定
# ==========================

if "page" not in st.session_state:
    st.session_state.page = "home"


# ==========================
# 画面中央寄せ設定
# ==========================

st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
        margin: auto;
        padding-top: 3rem;
    }

    h1 {
        text-align: center;
    }

    div.stButton {
        display: flex;
        justify-content: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# Gemini API設定
# ==========================
import streamlit as st
from google import genai

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# ==========================
# 初期設定
# ==========================

st.set_page_config(
    page_title="AI学習支援ツール",
    page_icon="📚",
    layout="wide"
)

DATA_DIR = "subjects"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ==========================
# セッション管理
# ==========================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

if "selected_lesson" not in st.session_state:
    st.session_state.selected_lesson = None

# ==========================
# AI学習機能用
# ==========================

# 授業問題
if "generated_question" not in st.session_state:
    st.session_state.generated_question = ""

if "grading_result" not in st.session_state:
    st.session_state.grading_result = ""

if "summary_result" not in st.session_state:
    st.session_state.summary_result = ""

if "important_result" not in st.session_state:
    st.session_state.important_result = ""

# ==========================
# 中間・期末テスト用
# ==========================

if "exam_question" not in st.session_state:
    st.session_state.exam_question = ""

if "exam_result" not in st.session_state:
    st.session_state.exam_result = ""

if "exam_count" not in st.session_state:
    st.session_state.exam_count = 0

if "exam_mode" not in st.session_state:
    st.session_state.exam_mode = ""

if "exam_history" not in st.session_state:
    st.session_state.exam_history = []

# ==========================
# 連続問題機能
# ==========================

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "total_score" not in st.session_state:
    st.session_state.total_score = 0

# ==========================
# 中間・期末テスト機能
# ==========================

if "exam_mode" not in st.session_state:
    st.session_state.exam_mode = ""

if "exam_question" not in st.session_state:
    st.session_state.exam_question = ""

if "exam_result" not in st.session_state:
    st.session_state.exam_result = ""

if "exam_count" not in st.session_state:
    st.session_state.exam_count = 0

if "exam_history" not in st.session_state:
    st.session_state.exam_history = []

# ==========================
# 保存関数
# ==========================

def save_subject(data):

    file_path = os.path.join(
        DATA_DIR,
        f"{data['subject_name']}.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


def load_subject(subject_name):

    file_path = os.path.join(
        DATA_DIR,
        f"{subject_name}.json"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def get_subject_list():

    subjects = []

    for file in os.listdir(DATA_DIR):

        if file.endswith(".json"):

            subjects.append(
                file.replace(".json", "")
            )

    return subjects

# ==========================
# テスト範囲取得
# ==========================

def get_midterm_material(data):

    material = ""

    try:

        end_lesson = int(
            data["midterm_range"]
        )

    except:

        end_lesson = (
            data["total_lessons"] // 2
        )

    for i in range(
        1,
        end_lesson + 1
    ):

        lesson_name = f"第{i}回"

        if lesson_name in data["lessons"]:

            material += f"""

【{lesson_name}】

{data["lessons"][lesson_name].get("text", "")}

{data["lessons"][lesson_name].get("note", "")}
"""

    return material


def get_final_material(data):

    material = ""

    for i in range(
        1,
        data["total_lessons"] + 1
    ):

        lesson_name = f"第{i}回"

        if lesson_name in data["lessons"]:

            material += f"""

【{lesson_name}】

{data["lessons"][lesson_name].get("text", "")}

{data["lessons"][lesson_name].get("note", "")}
"""

    return material

# ==========================
# ホーム画面
# ==========================

if st.session_state.page == "home":

    # ==========================
    # ホーム画面デザイン
    # ==========================

    st.markdown("""
    <style>

    /* ==========================
       ページ全体
       ========================== */

    .block-container {
        max-width: 900px;
        margin: auto;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ==========================
       タイトル
       ========================== */

    .home-title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .home-subtitle {
        text-align: center;
        font-size: 18px;
        color: #666666;
        margin-bottom: 30px;
    }


    /* ==========================
       セクションタイトル
       ========================== */

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 18px;
    }


    /* ==========================
       機能カード
       ========================== */

    .feature-title {
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
        white-space: nowrap;
    }

    .feature-description {
        text-align: center;
        font-size: 14px;
        line-height: 1.7;
        color: #555555;
    }


    /* ==========================
       スマホ対応
       ========================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1.5rem;
        }

        .home-title {
            font-size: 30px;
        }

        .home-subtitle {
            font-size: 15px;
            line-height: 1.6;
        }

        .section-title {
            font-size: 21px;
        }

        .feature-title {
            font-size: 19px;
        }

        .feature-description {
            font-size: 14px;
        }

    }

    </style>
    """, unsafe_allow_html=True)


    # ==========================
    # タイトル
    # ==========================

    st.markdown("""
    <div class="home-title">
        📚 AI学習支援サービス
    </div>

    <div class="home-subtitle">
        「分かったつもり」をなくし、効率的な復習をサポート
    </div>
    """, unsafe_allow_html=True)


    # ==========================
    # 使い方
    # ==========================

    with st.expander("❓ このサービスの使い方"):

        st.markdown("""
        **① 新しい教材を追加**

        授業名や講義資料（PDF）を登録します。

        **② 講義内容を整理**

        講義資料からAIが要約や重要ポイントを整理します。

        **③ 確認問題に挑戦**

        AIが講義内容から確認問題を作成します。

        **④ 復習する**

        確認問題などを活用して、理解が不十分な内容を復習します。
        """)


    # ==========================
    # このサービスでできること
    # ==========================

    st.markdown("""
    <div class="section-title">
        ✨ このサービスでできること
    </div>
    """, unsafe_allow_html=True)


    # ==========================
    # カード①・②
    # ==========================

    col1, col2 = st.columns(2)


    with col1:

        with st.container(border=True):

            st.markdown("""
            <div class="feature-title">
                ✨ AI要約
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-description">
                講義資料の内容をAIが整理し、<br>
                短時間で復習しやすくします。
            </div>
            """, unsafe_allow_html=True)


        with st.container(border=True):

            st.markdown("""
            <div class="feature-title">
                🎯 重要ポイント整理
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-description">
                講義資料から重要な内容を整理し、<br>
                学習すべきポイントを確認できます。
            </div>
            """, unsafe_allow_html=True)


    # ==========================
    # カード③・④
    # ==========================

    with col2:

        with st.container(border=True):

            st.markdown("""
            <div class="feature-title">
                📝 確認問題
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-description">
                AIが講義内容から問題を生成し、<br>
                自分の理解度を確認できます。
            </div>
            """, unsafe_allow_html=True)


        with st.container(border=True):

            st.markdown("""
            <div class="feature-title">
                🔄 復習ポイント
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-description">
                理解が不十分な内容を振り返り、<br>
                効率的な復習をサポートします。
            </div>
            """, unsafe_allow_html=True)


    # ==========================
    # 学習を始める
    # ==========================

    st.divider()

    st.markdown("""
    <div class="section-title">
        📖 学習を始める
    </div>
    """, unsafe_allow_html=True)


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "➕ 新しい教材を追加",
            width="stretch"
        ):

            st.session_state.page = "new_subject"
            st.rerun()


    with col2:

        if st.button(
            "📖 続きから学習",
            width="stretch"
        ):

            st.session_state.page = "resume"
            st.rerun()

# ==========================
# 新しい教科を追加
# ==========================

elif st.session_state.page == "new_subject":

    st.title("➕ 新しい教科を追加")

    st.write("授業の情報を登録してください。")


    # ==========================
    # 授業名
    # ==========================

    subject_name = st.text_input(
        "📘 授業名",
        placeholder="例：ミクロ経済学"
    )


    # ==========================
    # 授業回数
    # ==========================

    total_lessons = st.number_input(
        "📚 授業回数",
        min_value=1,
        max_value=30,
        value=15,
        step=1
    )


    st.divider()


    # ==========================
    # 中間テスト
    # ==========================

    st.subheader("📝 中間テスト")

    midterm = st.checkbox(
        "中間テストがある"
    )

    midterm_range = ""
    midterm_feature = ""

    if midterm:

        midterm_range = st.text_input(
            "中間テストの範囲",
            placeholder="例：第1回〜第7回"
        )

        midterm_feature = st.text_area(
            "中間テストの特徴",
            placeholder="例：記述問題が中心。計算問題も出題される。",
            height=100
        )


    st.divider()


    # ==========================
    # 期末テスト
    # ==========================

    st.subheader("📚 期末テスト")

    final_exam = st.checkbox(
        "期末テストがある"
    )

    final_range = ""
    final_feature = ""

    if final_exam:

        final_range = st.text_input(
            "期末テストの範囲",
            placeholder="例：第8回〜第15回"
        )

        final_feature = st.text_area(
            "期末テストの特徴",
            placeholder="例：授業内容をもとにした記述・応用問題が中心。",
            height=100
        )


    st.divider()


    # ==========================
    # 保存
    # ==========================

    if st.button(
        "💾 教科を登録する",
        width="stretch"
    ):

        if subject_name.strip() == "":

            st.warning("授業名を入力してください。")

        else:

            data = {

                "subject_name": subject_name,

                "total_lessons": total_lessons,

                "midterm": midterm,

                "midterm_range": midterm_range,

                "midterm_feature": midterm_feature,

                "final_exam": final_exam,

                "final_range": final_range,

                "final_feature": final_feature,

                "lessons": {}

            }


            # ==========================
            # 授業データを作成
            # ==========================

            for i in range(
                1,
                total_lessons + 1
            ):

                lesson_name = f"第{i}回"

                data["lessons"][lesson_name] = {

                    "status": "未登録",

                    "text": "",

                    "analysis": "",

                    "note": ""

                }


            # ==========================
            # 保存
            # ==========================

            save_subject(data)


            st.session_state.selected_subject = subject_name

            st.session_state.page = "subject"

            st.rerun()


    # ==========================
    # 戻る
    # ==========================

    if st.button("← ホームへ戻る"):

        st.session_state.page = "home"

        st.rerun()

# ==========================
# 教科一覧画面
# ==========================

elif st.session_state.page == "resume":

    st.title("📖 教科一覧")

    subjects = get_subject_list()

    if len(subjects) == 0:

        st.info("登録されている教科がありません")

    else:

        for subject in subjects:

            if st.button(f"📘 {subject}"):

                st.session_state.selected_subject = subject
                st.session_state.page = "subject"
                st.rerun()


    st.divider()


    if st.button("➕ 新しい教科を追加"):

        st.session_state.page = "new_subject"
        st.rerun()


    if st.button("← ホームへ戻る"):

        st.session_state.page = "home"
        st.rerun()



# ==========================
# 教科管理画面
# ==========================

elif st.session_state.page == "subject":


    if st.session_state.selected_subject is None:

        st.warning("教科を選択してください")

        st.session_state.page = "resume"
        st.rerun()



    data = load_subject(
        st.session_state.selected_subject
    )


    st.title(
        f"📘 {data['subject_name']}"
    )


    st.info(
        f"授業回数：{data['total_lessons']}回"
    )



    # ==========================
    # テスト対策
    # ==========================

    st.subheader("📝 テスト対策")


    col1, col2 = st.columns(2)


    with col1:

        if data["midterm"]:

            if st.button("📝 中間テスト対策"):

                st.session_state.test_mode = "midterm"


                st.session_state.test_material = (
                    get_midterm_material(data)
                )


                st.session_state.page = "midterm"

                st.rerun()



    with col2:

        if data["final_exam"]:

            if st.button("📚 期末テスト対策"):

                st.session_state.test_mode = "final"


                st.session_state.test_material = (
                    get_final_material(data)
                )


                st.session_state.page = "final"

                st.rerun()



    st.divider()



    # ==========================
    # 授業一覧
    # ==========================

    st.subheader("📖 授業一覧")


    registered_count = 0

    updated = False



    for i in range(
        1,
        data["total_lessons"] + 1
    ):


        lesson_name = f"第{i}回"



        if lesson_name not in data["lessons"]:


            data["lessons"][lesson_name] = {

                "status": "未登録",

                "text": "",

                "analysis": "",

                "note": ""

            }


            updated = True



        if (
            data["lessons"][lesson_name]["status"]
            == "登録済"
        ):

            registered_count += 1



    # 授業データを保存

    if updated:

        save_subject(data)



    # ==========================
    # 進捗表示
    # ==========================

    st.progress(
        registered_count / data["total_lessons"]
    )


    st.write(
        f"登録済み：{registered_count}/{data['total_lessons']}回"
    )



    st.divider()



    # ==========================
    # 授業ボタン
    # ==========================

    for i in range(
        1,
        data["total_lessons"] + 1
    ):


        lesson_name = f"第{i}回"


        status = (
            data["lessons"][lesson_name]["status"]
        )


        if status == "登録済":

            icon = "✅"

        else:

            icon = "📄"



        if st.button(
            f"{icon} {lesson_name} - {status}"
        ):


            st.session_state.selected_lesson = lesson_name

            st.session_state.page = "lesson"

            st.rerun()



    st.divider()



    if st.button("← 教科一覧へ戻る"):

        st.session_state.page = "resume"

        st.rerun()

# ==========================
# 授業ページ
# ==========================

elif st.session_state.page == "lesson":

    data = load_subject(
        st.session_state.selected_subject
    )

    lesson_name = st.session_state.selected_lesson


    # ==========================
    # AI結果リセット
    # ==========================

    if (
        "current_lesson" not in st.session_state
        or st.session_state.current_lesson != lesson_name
    ):

        st.session_state.summary_result = ""

        st.session_state.important_result = ""

        st.session_state.generated_question = ""

        st.session_state.grading_result = ""

        st.session_state.current_lesson = lesson_name



    st.title(
        f"{data['subject_name']} - {lesson_name}"
    )



    # ==========================
    # 既存データ取得
    # ==========================

    lesson_text = data["lessons"][lesson_name].get(
        "text",
        ""
    )


    lesson_note = data["lessons"][lesson_name].get(
        "note",
        ""
    )



    # ==========================
    # PDFアップロード
    # ==========================

    uploaded_file = st.file_uploader(
        "PDF資料をアップロード",
        type=["pdf"]
    )


    extracted_text = lesson_text



    if uploaded_file:


        reader = PdfReader(uploaded_file)

        extracted_text = ""


        for page in reader.pages:


            page_text = page.extract_text()


            if page_text:

                extracted_text += page_text



        st.success(
            f"{len(extracted_text)}文字抽出しました"
        )


        st.text_area(
            "抽出結果",
            extracted_text[:5000],
            height=250
        )



    # ==========================
    # 授業メモ
    # ==========================

    st.subheader("✍️ 授業メモ")


    lesson_note = st.text_area(
        "先生の発言や重要事項を記録",
        value=lesson_note,
        height=200
    )



    # ==========================
    # 保存
    # ==========================

    if st.button("💾 保存"):


        data["lessons"][lesson_name]["text"] = (
            extracted_text
        )


        data["lessons"][lesson_name]["note"] = (
            lesson_note
        )


        data["lessons"][lesson_name]["status"] = (
            "登録済"
        )


        save_subject(data)


        st.success("保存完了")

        st.rerun()



    # ==========================
    # AI用資料
    # ==========================

    study_material = f"""
【授業資料】

{data["lessons"][lesson_name].get("text", "")}


【授業メモ】

{lesson_note}
"""



    if (
        data["lessons"][lesson_name].get("text", "")
        != ""
    ):


        st.divider()


        st.subheader("🤖 AI学習サポート")



        col1, col2, col3 = st.columns(3)



        # ==========================
        # 要約
        # ==========================

        with col1:


            if st.button("📄 授業要約"):


                with st.spinner("要約中..."):


                    response = client.models.generate_content(

                        model="gemini-3.6-flash",

                        contents=f"""

以下を200文字程度で要約してください。


{study_material}

"""

                    )


                    st.session_state.summary_result = (
                        response.text
                    )



        # ==========================
        # 重要ポイント
        # ==========================

        with col2:


            if st.button("⭐ 重要ポイント"):


                with st.spinner("分析中..."):


                    response = client.models.generate_content(

                        model="gemini-3.6-flash",

                        contents=f"""

以下から重要ポイントを
5個抽出してください。


{study_material}

"""

                    )


                    st.session_state.important_result = (
                        response.text
                    )



        # ==========================
        # 問題生成
        # ==========================

        with col3:


            if st.button("📝 確認問題チャレンジ"):


                with st.spinner("問題作成中..."):


                    response = client.models.generate_content(

                        model="gemini-3.6-flash",

                        contents=f"""

あなたは大学教授です。


以下を基に
大学レベルの記述問題を
1問作成してください。


解答は表示しないこと。


{study_material}

"""

                    )


                    st.session_state.generated_question = (
                        response.text
                    )



        # ==========================
        # 要約結果
        # ==========================

        if st.session_state.summary_result:


            st.divider()


            st.subheader("📄 授業要約")


            st.markdown(
                st.session_state.summary_result
            )



        # ==========================
        # 重要ポイント結果
        # ==========================

        if st.session_state.important_result:


            st.divider()


            st.subheader("⭐ 重要ポイント")


            st.markdown(
                st.session_state.important_result
            )



        # ==========================
        # 問題表示
        # ==========================

        if st.session_state.generated_question:


            st.divider()


            st.subheader("📝 確認問題")


            st.markdown(
                st.session_state.generated_question
            )


            answer = st.text_area(
                "あなたの回答",
                height=200
            )



            if st.button("📊 採点する"):


                with st.spinner("採点中..."):


                    result = client.models.generate_content(

                        model="gemini-3.6-flash",

                        contents=f"""

あなたは大学教授です。


問題

{st.session_state.generated_question}



学生回答

{answer}



模範解答も示しながら
以下の形式で評価してください。



【得点】

100点満点



【模範解答】



【解説】



【復習すべきポイント】



【理解度コメント】

"""

                    )


                    st.session_state.grading_result = (
                        result.text
                    )



        # ==========================
        # 採点結果
        # ==========================

        if st.session_state.grading_result:


            st.divider()


            st.subheader("📊 採点結果")


            st.markdown(
                st.session_state.grading_result
            )



            if st.button("➡ 次の問題へ"):


                st.session_state.generated_question = ""

                st.session_state.grading_result = ""

                st.rerun()



    st.divider()



    if st.button("← 授業一覧へ戻る"):


        st.session_state.page = "subject"

        st.rerun()

# ==========================
# 中間テスト対策ページ
# ==========================

elif st.session_state.page == "midterm":

    data = load_subject(
        st.session_state.selected_subject
    )


    st.title(
        f"📝 {data['subject_name']} 中間テスト対策"
    )


    material = st.session_state.test_material


    st.info(
        "中間テスト範囲をAIで復習し、確認問題に挑戦できます"
    )



    # ==========================
    # AI復習・問題生成
    # ==========================

    col1, col2, col3 = st.columns(3)



    # ==========================
    # AI総復習
    # ==========================

    with col1:

        if st.button("📚 AI総復習"):


            with st.spinner("復習資料を作成中..."):


                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=f"""

あなたは大学教授です。

以下は中間テスト範囲の授業内容です。

学生が試験前に復習できるように、
重要事項を整理してください。


【出力形式】

・授業全体の流れ

・重要概念

・覚えるべきポイント

・試験に出やすい内容

・注意点



【テスト範囲】

{material}

"""

                )


                st.session_state.midterm_review = (
                    response.text
                )



    # ==========================
    # 重要ポイント
    # ==========================

    with col2:

        if st.button("⭐ 重要ポイント"):


            with st.spinner("分析中..."):


                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=f"""

以下の中間テスト範囲から
重要ポイントを5つ抽出してください。


出力形式：

①重要ポイント

②理由

③覚え方


【テスト範囲】

{material}

"""

                )


                st.session_state.midterm_points = (
                    response.text
                )



    # ==========================
    # 問題生成
    # ==========================

    with col3:

        if st.button("📝 確認問題チャレンジ"):


            with st.spinner("問題作成中..."):


                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=f"""

あなたは大学教授です。

以下は中間テスト範囲です。

大学レベルの確認問題を
1問作成してください。


条件：

・記述問題

・考え方を問う問題

・解答は表示しない



【テスト範囲】

{material}

"""

                )


                st.session_state.midterm_question = (
                    response.text
                )



    # ==========================
    # 復習結果表示
    # ==========================

    if (
        "midterm_review" in st.session_state
        and st.session_state.midterm_review
    ):


        st.divider()


        st.subheader("📚 AI総復習")


        st.markdown(
            st.session_state.midterm_review
        )



    # ==========================
    # 重要ポイント表示
    # ==========================

    if (
        "midterm_points" in st.session_state
        and st.session_state.midterm_points
    ):


        st.divider()


        st.subheader("⭐ 重要ポイント")


        st.markdown(
            st.session_state.midterm_points
        )



    # ==========================
    # 問題表示
    # ==========================

    if (
        "midterm_question" in st.session_state
        and st.session_state.midterm_question
    ):


        st.divider()


        st.subheader("📝 確認問題")


        st.markdown(
            st.session_state.midterm_question
        )



        answer = st.text_area(
            "あなたの回答",
            height=200
        )



        # ==========================
        # 採点
        # ==========================

        if st.button("📊 採点する"):


            with st.spinner("採点中..."):


                result = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=f"""

あなたは大学教授です。


問題

{st.session_state.midterm_question}



学生回答

{answer}



以下の形式で評価してください。



【得点】

100点満点



【模範解答】



【解説】



【復習ポイント】



【理解度コメント】


"""

                )


                st.session_state.midterm_result = (
                    result.text
                )



    # ==========================
    # 採点結果
    # ==========================

    if (
        "midterm_result" in st.session_state
        and st.session_state.midterm_result
    ):


        st.divider()


        st.subheader("📊 採点結果")


        st.markdown(
            st.session_state.midterm_result
        )



        if st.button("➡ 次の問題へ"):


            st.session_state.midterm_question = ""

            st.session_state.midterm_result = ""

            st.rerun()



    st.divider()



    if st.button("← 教科画面へ戻る"):


        st.session_state.page = "subject"

        st.rerun()

# ==========================
# 期末テスト対策ページ
# ==========================

elif st.session_state.page == "final":

    data = load_subject(
        st.session_state.selected_subject
    )


    st.title(
        f"📚 {data['subject_name']} 期末テスト対策"
    )


    material = st.session_state.test_material


    st.info(
        "全授業範囲をAIで復習し、確認問題に挑戦できます"
    )



    # ==========================
    # AI機能
    # ==========================

    col1, col2, col3 = st.columns(3)



    # ==========================
    # AI総復習
    # ==========================

    with col1:


        if st.button("📚 AI総復習"):


            with st.spinner("復習資料を作成中..."):


                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=f"""

あなたは大学教授です。

以下は期末テスト範囲の授業内容です。

学生が試験前に全範囲を復習できるように、
体系的に整理してください。


【出力形式】

・授業全体の流れ

・重要概念

・関連する考え方

・試験に出やすいポイント

・注意点



【テスト範囲】

{material}

"""

                )


                st.session_state.final_review = (
                    response.text
                )



    # ==========================
    # 重要ポイント
    # ==========================

    with col2:


        if st.button("⭐ 重要ポイント"):


            with st.spinner("分析中..."):


                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=f"""

以下の期末テスト範囲から
重要ポイントを5つ抽出してください。


出力形式：

①重要ポイント

②理由

③試験対策



【テスト範囲】

{material}

"""

                )


                st.session_state.final_points = (
                    response.text
                )



    # ==========================
    # 確認問題生成
    # ==========================

    with col3:


        if st.button("📝 確認問題チャレンジ"):


            with st.spinner("問題作成中..."):


                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=f"""

あなたは大学教授です。


以下は期末テスト範囲です。


大学レベルの確認問題を
1問作成してください。


条件：

・記述問題

・応用問題

・計算問題も含める

・解答は表示しない



【テスト範囲】

{material}

"""

                )


                st.session_state.final_question = (
                    response.text
                )



    # ==========================
    # 復習結果
    # ==========================

    if (
        "final_review" in st.session_state
        and st.session_state.final_review
    ):


        st.divider()


        st.subheader("📚 AI総復習")


        st.markdown(
            st.session_state.final_review
        )



    # ==========================
    # 重要ポイント表示
    # ==========================

    if (
        "final_points" in st.session_state
        and st.session_state.final_points
    ):


        st.divider()


        st.subheader("⭐ 重要ポイント")


        st.markdown(
            st.session_state.final_points
        )



    # ==========================
    # 問題表示
    # ==========================

    if (
        "final_question" in st.session_state
        and st.session_state.final_question
    ):


        st.divider()


        st.subheader("📝 確認問題")


        st.markdown(
            st.session_state.final_question
        )


        answer = st.text_area(
            "あなたの回答",
            height=200
        )




        if st.button("📊 採点する"):


            with st.spinner("採点中..."):


                result = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=f"""

あなたは大学教授です。


問題

{st.session_state.final_question}



学生回答

{answer}



以下の形式で評価してください。



【得点】

100点満点



【模範解答】



【解説】



【復習ポイント】



【理解度コメント】


"""

                )


                st.session_state.final_result = (
                    result.text
                )



    # ==========================
    # 採点結果
    # ==========================

    if (
        "final_result" in st.session_state
        and st.session_state.final_result
    ):


        st.divider()


        st.subheader("📊 採点結果")


        st.markdown(
            st.session_state.final_result
        )



        if st.button("➡ 次の問題へ"):


            st.session_state.final_question = ""

            st.session_state.final_result = ""

            st.rerun()


    st.divider()



    if st.button("← 教科画面へ戻る"):


        st.session_state.page = "subject"

        st.rerun()