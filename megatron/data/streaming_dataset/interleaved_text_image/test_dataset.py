from transformers import GPT2Tokenizer
from sympy.physics.units.definitions.dimension_definitions import current

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

bos_tokens = -3
eos_tokens = 1000000000

max_length = 77
data = {}


data["text"] = ["john is going to the",None," and then all of the cacti will be lit",None, "in glorious sacred fire"]
data["images"] = [None,1,None,2,None]

data = [data]

image_buffer = []
text_buffer = []
total_buffer = 0

def potato():
    
    for sample in data:
        text = sample["text"]
        images = sample["images"]
        
        text_buffer.append([bos_tokens])
        
        for section in text:
            if section != None:
            #Need to check this for max length however
                text_buffer.append(tokenizer(section, truncation=False,padding=False)["input_ids"])
            else:
                text_buffer.append(None)
        
        image_buffer.insert(0, None)#To batch bos
        image_buffer.extend(images)
        image_buffer.append(eos_tokens)
        text_buffer.append(None)#match image eos
        
        print(text_buffer)
        print(image_buffer)
        
        #We want to add text and image to our upcoming output (setup), and remove them from the buffer.
        
        current_length = 0
        curr_text = []
        curr_image = []
        while True:
            
            print("Current lists", curr_text, curr_image)
            
            text = text_buffer[0]
            image = image_buffer[0]
            
            print("Newest", text, image)
                    
            if text == None and image == None:
                print("Uhoh, double none")
                exit()
            elif text != None and image != None:
                print("Uhoh, double NOT none")
                exit()
            elif text != None and image == None:
                #Fix saving the missing/original part of the text
                if current_length + len(text) > max_length:#Too long, that's fine for text, just grab what we can
                    current_length = max_length
                    text_append = text[:current_length + len(text) - max_length]#Changes the actual list in the thing
                    text[0] = text[current_length + len(text) - max_length:]
                    #We do NOT pop an image here because we haven't finished the current text
                    #We also naturally do not pop text.
                    
                else:#Not greater, remove entire text and entire image
                    text_append = text_buffer.pop(0)
                    image_buffer.pop(0)#Just remove the None for image
                    current_length += len(text_append)
                    
                curr_text.extend(text_append)
                curr_image.append(None)
                
            #TODO what do we do if we exactly are in range to fit an image, but not the image EOS?
            elif text == None and image != None:
                #Number might be 67 instead.
                #Should we even add on images?
                if current_length + 66 + 10 > max_length:#Nothing we can do for text, just pad instead
                    #We are just going to yield
                    current_length = max_length
                    
                        
                else:#So this includes that EOS case...
                    curr_image.append(image_buffer.pop(0))
                    curr_text.append(text_buffer.pop(0))
                    current_length += 66
            else:
                print("No clue")
                exit()
            
            if current_length == max_length:
                #TODO needs to do multimodal positioning and some other stuff
                pass
                
            elif current_length > max_length:
                print("went over length somehow, check code again")
                exit()
        exit()
        
        
        
        return {
                    # convert to bytes to store in MDS binary format
                    'tokens': text_buffer,
                    'images': image_buffer,
                    'multimodal_position_ids': multimodal_position_ids,
                    'labels': labels,
                }
            

potato()