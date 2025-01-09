import random
import pandas as pd
from chatgpt_helper import get_chatgpt_response

# Define Yin and Yang
def get_yin_yang(outcomes, mapping_df):
    # Count the number of tails (0s) in the throw
    num_tails = sum(1 for coin in outcomes if coin == 0)
    row = mapping_df[mapping_df["硬币"] == num_tails].iloc[0]
    return row["名称"], row["图案"], row["阴阳"], row["YinYang_code"], row["动静"]

def main():
    print("欢迎使用金钱卦占卜系统！")

    # 获取用户占卜主题
    topic = input("请告诉我你想要占卜的主题：")

    # 加载CSV数据 
    mapping_df = pd.read_csv("yin_yang_mapping.csv")

    # 投掷硬币六次，记录结果
    results = []

    for i in range(6):
        input(f"现在是第 {i + 1} 爻，你准备好投掷铜钱了吗？请保持静心、诚挚、意念专一（输入'y'开始）：")
        coins = [random.randint(0, 1) for _ in range(3)]  # 随机生成 0 或 1，表示正反面
        name, symbol, yin_yang, yinyang_code, movement = get_yin_yang(coins, mapping_df)
        
        results.append({
            "爻位": i + 1,  # 初爻为1，上爻为6
            "名称": name, 
            "阴阳": yin_yang,      # Chinese characters (阴/阳)
            "YinYang_code": yinyang_code,  # Symbols (⚋/⚊)
            "图案": symbol,
            "动静": movement
        })

        print(f"第 {i + 1} 爻的结果：{symbol} （{name}）")

    input("\n六爻已完成。输入任意键显示卦象详细信息：")
   
    # 生成变卦
    transformed_results = []
    for result in results:
        if result["动静"] == "动":
            # 阴变阳，阳变阴
            new_yin_yang = "阳" if result["阴阳"] == "阴" else "阴"
            new_symbol = "⚊" if new_yin_yang == "阳" else "⚋"
            transformed_results.append(new_symbol)
        else:
            transformed_results.append(result["图案"])


    # 记录卦象信息
    main_gua = []
    bian_gua = []
    
    for result in reversed(results):  # Reverse to match traditional bottom-to-top display
        # 记录主卦信息
        main_info = {
            "爻位": result["爻位"],
            "名称": result["名称"],
            "图案": result["图案"],
            "阴阳": result["阴阳"],
            "YinYang_code": result["YinYang_code"],
            "动静": result["动静"]
        }
        main_gua.append(main_info)
        
        # 记录变卦信息
        new_yinyang = "阳" if result["阴阳"] == "阴" and result["动静"] == "动" else "阴" if result["阴阳"] == "阳" and result["动静"] == "动" else result["阴阳"]
        new_symbol = "⚊" if new_yinyang == "阳" else "⚋"
        
        bian_info = {
            "爻位": result["爻位"],
            "名称": "老阳" if new_yinyang == "阳" and result["动静"] == "动" else 
                   "老阴" if new_yinyang == "阴" and result["动静"] == "动" else
                   "少阳" if new_yinyang == "阳" else "少阴",
            "图案": new_symbol,
            "阴阳": new_yinyang,
            "YinYang_code": new_symbol,
            "动静": result["动静"]
        }
        bian_gua.append(bian_info)


    # 分析主卦的上下卦
    main_upper = [yao for yao in main_gua if yao["爻位"] in [6, 5, 4]]  # 上卦
    main_lower = [yao for yao in main_gua if yao["爻位"] in [3, 2, 1]]  # 下卦
    
    # 分析变卦的上下卦
    bian_upper = [yao for yao in bian_gua if yao["爻位"] in [6, 5, 4]]  # 上卦
    bian_lower = [yao for yao in bian_gua if yao["爻位"] in [3, 2, 1]]  # 下卦

    # Store all hexagram information
    hexagram_info = {
        "主卦": {
            "完整卦": main_gua,
            "上卦": main_upper,
            "下卦": main_lower
        },
        "变卦": {
            "完整卦": bian_gua,
            "上卦": bian_upper,
            "下卦": bian_lower
        }
    }


    # Read bagua mapping data
    bagua_df = pd.read_csv('bagua_mapping.csv')

    # Helper function to get bagua name from trigram symbols
    def get_bagua_name(trigram_symbols):
        # Convert trigram symbols to string for comparison
        trigram_pattern = ''.join([yao["YinYang_code"].strip() for yao in trigram_symbols])
        
        # Search through bagua mapping
        for _, row in bagua_df.iterrows():
            bagua_pattern = (''.join([row['6'], row['5'], row['4']]) if len(trigram_symbols) == 3 
                            else ''.join([row['3'], row['2'], row['1']]))
            if bagua_pattern == trigram_pattern:
                return row['Name'], row['Nature']
        return None, None

    # Get bagua names for main hexagram
    main_upper_name, main_upper_nature = get_bagua_name(main_upper)
    main_lower_name, main_lower_nature = get_bagua_name(main_lower)

    # Get bagua names for changed hexagram
    bian_upper_name, bian_upper_nature = get_bagua_name(bian_upper)
    bian_lower_name, bian_lower_nature = get_bagua_name(bian_lower)

    # Read 64 gua mapping data
    gua64_df = pd.read_csv('64gua_mapping.csv')

    # Get the complete hexagram names from the 64 gua mapping
    def get_complete_gua_name(upper_name, lower_name):
        try:
            return gua64_df.loc[gua64_df['Unnamed: 0'] == upper_name, lower_name].values[0]
        except:
            return None

    # Get complete hexagram names for both main and changed hexagrams
    main_complete_name = get_complete_gua_name(main_upper_name, main_lower_name)
    bian_complete_name = get_complete_gua_name(bian_upper_name, bian_lower_name)

    print(f"\n完整卦象:")
    print(f"主卦: {main_complete_name}")
    print(f"变卦: {bian_complete_name}")

    # Print hexagrams side by side
    print("\n卦象：")
    print("主卦    变卦")
    
    # Since we want to display from top to bottom
    for i in range(5, -1, -1):  # from 6 to 1
        main_yao = next(yao for yao in main_gua if yao["爻位"] == i + 1)
        bian_yao = next(yao for yao in bian_gua if yao["爻位"] == i + 1)
        
        # Add dynamic marks: 'o' for 老阳, 'x' for 老阴, only one mark per yao
        dynamic_mark = " o" if main_yao["动静"] == "动" and main_yao["图案"] == "⚊" else \
                      " x" if main_yao["动静"] == "动" and main_yao["图案"] == "⚋" else \
                      "  "
        
        print(f"{main_yao['图案']}{dynamic_mark}    {bian_yao['图案']}")

    # Read 64 gua explanations data
    gua64_exp_df = pd.read_csv('64gua_exp.csv')

    # Get the gua number for main and changed hexagrams
    main_gua_num = gua64_df.loc[gua64_df['Unnamed: 0'] == main_upper_name, main_lower_name].index[0] + 1
    bian_gua_num = gua64_df.loc[gua64_df['Unnamed: 0'] == bian_upper_name, bian_lower_name].index[0] + 1

    # Get the corresponding texts from 64gua_exp.csv
    gua_exp_df = pd.read_csv('64gua_exp.csv')
    
    # Get main gua explanation by matching the hexagram name
    main_exp = gua_exp_df[gua_exp_df['卦象'] == main_complete_name].iloc[0]
    main_zhouyi = main_exp['周易经文']
    main_translation = main_exp['译文']

    # Get bian gua explanation by matching the hexagram name
    bian_exp = gua_exp_df[gua_exp_df['卦象'] == bian_complete_name].iloc[0]
    bian_zhouyi = bian_exp['周易经文']
    bian_translation = bian_exp['译文']

    print("\n主卦解析:")
    print(f"上卦: {main_upper_name}({main_upper_nature})")
    print(f"下卦: {main_lower_name}({main_lower_nature})")
    print(f"完整卦象: {get_complete_gua_name(main_upper_name, main_lower_name)}")
    print(f"周易经文: {main_zhouyi}")

    print("\n变卦解析:")
    print(f"上卦: {bian_upper_name}({bian_upper_nature})")
    print(f"下卦: {bian_lower_name}({bian_lower_nature})")
    print(f"完整卦象: {get_complete_gua_name(bian_upper_name, bian_lower_name)}")
    print(f"周易经文: {bian_zhouyi}")

    # After printing all hexagram information
    input("\n输入任意键生成AI卦象解读：")
    print("\n正在生成卦象解读...")
    
    # Create the prompt with actual values
    prompt = f"""
你是一位精通《周易》卦象解读的占卜师。以下是一次完整的卜卦信息，你需要根据提供的内容分析并回答：

1. {topic}：这是占卜者想要了解的问题
2. {main_complete_name}：表示当前的状况
3. {main_zhouyi}：主卦的《周易》经文
4. {main_translation}：主卦的解释，帮助你理解当前的状况
5. {bian_complete_name}：表示未来的发展趋势或结果
6. {bian_zhouyi}：变卦的《周易》经文
7. {bian_translation}：变卦的解释，帮助你理解未来的趋势

请根据主卦译文描述现在的状况，根据变卦译文分析未来可能的发展趋势。结合两者分析卜卦者的事情应如何应对，并提供以下内容：

- 当前状况：根据主卦译文描述
- 未来趋势：根据变卦译文预测事情的发展可能
- 建议：分析主卦和变卦间的关系，给出具体建议。若主卦与变卦和谐，说明如何维持良好趋势；若主卦与变卦冲突，指出占卜者需要如何调整行为或心态以实现目标。

请详细分析并生成解读和建议。
"""

    # Get the explanation from ChatGPT
    explanation = get_chatgpt_response(prompt)

    # Print the divination explanation
    print("\nAI占卜：")
    print("=" * 50)
    print(explanation)
    print("=" * 50)


if __name__ == "__main__":
    main()