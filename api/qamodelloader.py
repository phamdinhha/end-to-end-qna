import torch
from transformers import AlbertTokenizer, AlbertForQuestionAnswering
from transformers import BertTokenizer, BertForQuestionAnswering


path = "D:/Deep_learning/Workspace/Question_Answering_System/model/best_model_2/"
# model = QuestionAnsweringModel('bert', model_path, use_cuda=False)

class QAModelLoader:

    def __init__(self, model_path = 'D:/Deep_learning/Workspace/Question_Answering_System/model/best_model_2/'):
        self.tokenizer = BertTokenizer.from_pretrained('D:/Deep_learning/Workspace/Question_Answering_System/model/best_model_2/')
        self.model = BertForQuestionAnswering.from_pretrained('D:/Deep_learning/Workspace/Question_Answering_System/model/best_model_2/')

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


