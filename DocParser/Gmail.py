from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from pprint import pprint
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']



def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id, q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError:
    print ('An error occurred')

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    return message
  except errors.HttpError:
    print ('An error occurred') 

def GetAttachments(service, user_id, msg_id, store_dir):
  """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    for part in message['payload']['parts']:
      if part['filename']:
        attachment_id=part['body']['attachmentId']
        attachment_data=service.users().messages().attachments().get(id=attachment_id, messageId=msg_id,userId=user_id).execute()['data']
        file_data = base64.urlsafe_b64decode(attachment_data.encode('UTF-8'))
        path = ''.join([store_dir, part['filename']])
        # print(file_data)
        f = open(path, 'wb')

        f.write(file_data)
        f.close()

  except errors.HttpError as e:
    print('An error occurred %s',e)

def CreateLabel(service, user_id, label_object):
  """Creates a new label within user's mailbox, also prints Label ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_object: label to be added.

  Returns:
    Created Label.
  """
  try:
    label = service.users().labels().create(userId=user_id,body=label_object).execute()
    print(label['id'])	
    return label
  except errors.HttpError:
    print ('An error occurred')


def MakeLabel(label_name, mlv='show', llv='labelShow'):
  """Create Label object.

  Args:
    label_name: The name of the Label.
    mlv: Message list visibility, show/hide.
    llv: Label list visibility, labelShow/labelHide.

  Returns:
    Created Label.
  """
  label = {'messageListVisibility': mlv,
           'name': label_name,
           'labelListVisibility': llv}
  return label

def ModifyMessage(service, user_id, msg_id, msg_labels):
  """Modify the Labels on the given Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The id of the message required.
    msg_labels: The change in labels.

  Returns:
    Modified message, containing updated labelIds, id and threadId.
  """
  try:
    message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                body=msg_labels).execute()

    label_ids = message['labelIds']
    return message
  except errors.HttpError as e:
    print('An error occurred %s',e)


def CreateMsgLabels(new_label_id):
  """Create object to update labels.

  Returns:
    A label update object.
  """
  return {'removeLabelIds': ['UNREAD','INBOX','CATEGORY_PERSONAL'], 'addLabelIds': [new_label_id]}

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    user_id = 'akshay.raut211@gmail.com'
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    new_label_name='Jatanapublished'
    new_label_id=''
    label_list_data=service.users().labels().list(userId=user_id).execute()['labels']
    label_list=[label for label in label_list_data if label['name']==new_label_name]

    if len(label_list)==0:
        label_object = MakeLabel(new_label_name)
        new_label_id=CreateLabel(service,user_id,label_object)['id']
    else:
        new_label_id=label_list[0]['id']
    
    msglist = ListMessagesMatchingQuery(service,user_id,'subject:Fwd: articles for Nov 3 Janata from:halleshubham@gmail.com label:inbox')
    message_id_list=[msg['id'] for msg in msglist]
    messages=[]
    for msg_id in message_id_list:
        messages.append(GetMessage(service,user_id,msg_id))
    pprint(messages[0]['labelIds'])
    for msg_id in message_id_list:
        GetAttachments(service,user_id,msg_id,'')
        msg_labels=CreateMsgLabels(new_label_id)
        ModifyMessage(service,user_id,msg_id,msg_labels)
    

   

if __name__ == '__main__':
    main()


