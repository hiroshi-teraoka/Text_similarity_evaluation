from sumeval.metrics.bleu import BLEUCalculator
from sumeval.metrics.rouge import RougeCalculator
import pandas as pd
import sys


class TextEvaluation:
    """
    テキストの類似度評価
    """
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        # input_file_name = 'input_excel/input_files.xlsx'

    def convert_excel_to_df_and_evaluate(self):
        """エクセルをDataFrameへ"""
        input_df = pd.ExcelFile(self.input_file).parse()

        bleu_ja = BLEUCalculator(lang="ja")
        rouge = RougeCalculator(lang="ja")
        output_dict = {'bleu':[], 'rouge_1':[], 'rouge_2':[], 'rouge_long':[]}
        for index, row in input_df.iterrows():
            output_dict['bleu'].append(bleu_ja.bleu(row['ref_text'], row['input_text']))  # BLEUでの評価
            output_dict['rouge_1'].append(rouge.rouge_n(summary=row['ref_text'], references=row['input_text'], n=1))  # ROUGE(n1)での評価
            output_dict['rouge_2'].append(rouge.rouge_n(summary=row['ref_text'], references=row['input_text'], n=2))  # ROUGE(n2)での評価
            output_dict['rouge_long'].append(rouge.rouge_l(summary=row['ref_text'], references=row['input_text']))       # ROUGE(rouge_l)での評価
            # input_microphone_df['rouge_be'] = rouge.rouge_be(summary=row['ref_text'], references=row['input_text'])      # ROUGE(rouge_be)での評価

        input_df['bleu']=output_dict['bleu']
        input_df['rouge_1']=output_dict['rouge_1']
        input_df['rouge_2']=output_dict['rouge_2']
        input_df['rouge_long']=output_dict['rouge_long']
        # print(input_df)
        return input_df

    def output_df_to_excel(self, df):
        """DataFrameをエクセルで出力"""
        # df.to_excel('output_excel/output.xlsx')
        df.to_excel(self.output_file)


if __name__ == '__main__':
    """
    実行方法
    (venv)$ python mimiClient_ASRtest.py 'application_id' 'client_id' 'client_secletkey' '入力音声ファイルパス.raw' '出力音声ファイルパス(output_folder/ .txtなど)'
    """
    args = sys.argv
    # print(args[1], args[2])
    text_evaluation = TextEvaluation(args[1], args[2])
    input_data = text_evaluation.convert_excel_to_df_and_evaluate()
    text_evaluation.output_df_to_excel(input_data)
