import numpy as np
import pandas as pd
from scipy.special import softmax

from simpletransformers.ner import NERModel, NERArgs

# Creating train_df  and eval_df for demonstration
train_data = [[0, "Simple", "B-MISC"], [0, "Transformers", "I-MISC"], [0, "started", "O"], [0, "with", "O"],
              [0, "text", "O"], [0, "classification", "B-MISC"], [1, "Simple", "B-MISC"], [1, "Transformers", "I-MISC"],
              [1, "can", "O"], [1, "now", "O"], [1, "perform", "O"], [1, "NER", "B-MISC"], ]
train_df = pd.DataFrame(train_data, columns=["sentence_id", "words", "labels"])

eval_data = [[0, "Simple", "B-MISC"], [0, "Transformers", "I-MISC"], [0, "was", "O"], [0, "built", "O"],
             [0, "for", "O"], [0, "text", "O"], [0, "classification", "B-MISC"], [1, "Simple", "B-MISC"],
             [1, "Transformers", "I-MISC"], [1, "then", "O"], [1, "expanded", "O"], [1, "to", "O"], [1, "perform", "O"],
             [1, "NER", "B-MISC"], ]
eval_df = pd.DataFrame(eval_data, columns=["sentence_id", "words", "labels"])

# # Create a NERModel
# model = NERModel(
#     "bert",
#     "bert-base-cased",
#     args={"overwrite_output_dir": True, "reprocess_input_data": True, "use_multiprocessing": False,
#           "dataloader_num_workers": 0, "process_count": 1, "use_multiprocessing_for_evaluation": False},
#     use_cuda=False
# )

model_args = NERArgs()
model_args.classification_report = True
model_args.silent = True
model_args.num_train_epochs = 2

model_args.process_count = 1
model_args.use_multiprocessing = False
model_args.overwrite_output_dir = True
model_args.dataloader_num_workers = 0
model_args.use_multiprocessing_for_evaluation = False
model_args.reprocess_input_data = True
model_args.evaluate_during_training = True
model_args.save_model_every_epoch = False
model_args.save_eval_checkpoints = False
model_args.save_steps = -1

# Create a NERModel
model = NERModel("bert", "bert-base-cased", args=model_args, use_cuda=False)

# Train the model
model.train_model(train_df, eval_data=eval_df)

# Evaluate the model
# result, model_outputs, predictions = model.eval_model(eval_df)

# Predictions on arbitary text strings
sentences = ["Some arbitary sentence", "Simple Transformers sentence"]
predictions, raw_outputs = model.predict(sentences)

print(predictions)

# More detailed preditctions
for n, (preds, outs) in enumerate(zip(predictions, raw_outputs)):
    print("\n___________________________")
    print("Sentence: ", sentences[n])
    for pred, out in zip(preds, outs):
        key = list(pred.keys())[0]
        new_out = out[key]
        preds = list(softmax(np.mean(new_out, axis=0)))
        print(key, pred[key], preds[np.argmax(preds)], preds)
