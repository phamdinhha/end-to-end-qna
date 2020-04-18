import torch
from transformers import AlbertTokenizer, AlbertForQuestionAnswering
from transformers import BertTokenizer, BertForQuestionAnswering


model_path = "path_to_your_model"


class QAModelLoader:

    def __init__(self, model_path = model_path):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForQuestionAnswering.from_pretrained(model_path)

    def answer(self, question, text):
        input_dict = self.tokenizer.encode_plus(question, text, return_tensors='pt', max_length=512)
        input_ids = input_dict["input_ids"].tolist()
        start_scores, end_scores = self.model(**input_dict)

        start = torch.argmax(start_scores, dim=1)
        end = torch.argmax(end_scores, dim=1)

        all_tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        answer = ''.join(all_tokens[start: end + 1]).replace('▁', ' ').strip()
        answer = answer.replace('[SEP]', '')
        return answer if answer != '[CLS]' and len(answer) != 0 else 'could not find an answer'


