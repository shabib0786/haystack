import logging

class OmniChannelResponseUtil:

    @staticmethod
    def get_response(text: str, image: str, video: str, sender: str):
        if image!=None and len(image)==0:
            image = None
        if video!=None and len(video)==0:
            video = None

        logging.info(f'IN get response======TEXT : {text}, IMAGE : {image}, VIDEO : {video}=============')
        if text!= None and image!=None and video!= None:
            return [{"recipient_id": sender , "image": image}, {"recipient_id": sender , "text" : text}, {"recipient_id": sender, "custom" : { "attachment" : { "type":"video", "payload":{ "src": video } }} }]
       
        elif text!=None and image!=None:
            return [{"recipient_id": sender , "image": image}, {"recipient_id": sender , "text" : text}]
       
        elif text!=None and video!=None:
            return [{"recipient_id": sender , "text" : text}, {"recipient_id": sender, "custom" : { "attachment" : { "type":"video", "payload":{ "src": video } }} }]
        
        elif image!=None and video!=None:
            return [{"recipient_id": sender , "image": image}, {"recipient_id": sender, "custom" : { "attachment" : { "type":"video", "payload":{ "src": video } }} }]
       
        elif text!=None:
            return [{"recipient_id": sender , "text" : text}]
       
        elif image!=None:
            return [{"recipient_id": sender , "image": image}]
       
        elif video!=None:
            return [{"recipient_id": sender, "custom" : { "attachment" : { "type":"video", "payload":{ "src": video } }} }]
