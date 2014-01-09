__author__ = 'Chris Seto'


from os.path import basename

from boto.exception import *
from boto.s3.connection import *
import os


class BucketManager:
    "S3 Bucket management"
    def __init__(self, connect=S3Connection):
        self.connection = connect
        if(len(self.connection.get_all_buckets()) == 0):
            self.newBucket("DefaultBucket")
        else:
            self.__defaultBucket = self.connection.get_all_buckets()[1]

    @staticmethod
    def getLoctions(self):
        print '\n'.join(i for i in dir(Location) if i[0].isupper())

    def __getProperBucket(self,bucket):
        if(bucket is None):
            return self.__defaultBucket
        else:
            return self[bucket]

    def newBucket(self, name,location=Location.DEFAULT):
        try:
            self.connection.create_bucket(name.lower(),location)
        except S3CreateError:
            print "S3CreateError: Bucket name already in use."

    def changeDefaultBucket(self,bucketName):
        try:
            self.__defaultBucket = self[bucketName]
        except Exception:
            self.newBucket(bucketName)
            self.__defaultBucket = self[bucketName]

    def getBucket(self,bucketName):
        try:
            return self.connection.get_bucket(bucketName.lower())
        except S3PermissionsError:
            print S3PermissionsError.message

    def __getitem__(self, item):
        return self.getBucket(item)

    def listBuckets(self):
       list = self.connection.get_all_buckets()
       for bucket in list:
            print bucket

    def createKey(self,key,bucket):
        Key(self[bucket]).key = key

    def uploadFile(self,fileName,bucket=None,pathToFolder=""):
        if(bucket is None):
            k = Key(self.__defaultBucket)
        else:
            k = Key(self[bucket])
        k.key = pathToFolder + basename(fileName)
        k.set_contents_from_filename(fileName)

    def downloadFile(self,fileName,bucket=None):
        if(bucket is None):
            k = Key(self.__defaultBucket)
        else:
            k = Key(self[bucket])
        k.key = fileName
        k.get_contents_to_file(open("/Users/nan/Downloads/" + fileName,'a'))

    def postString(self,title,contents,bucket=None,pathToFolder=""):
        if(bucket is None):
            k = Key(self.__defaultBucket)
        else:
            k = Key(self[bucket])
        k.key = pathToFolder + title
        k.set_contents_from_string(contents)

    def getString(self,title,bucket=None):
        if(bucket is None):
            k = Key(self.__defaultBucket)
        else:
            k = Key(self[bucket])
        k.key = title
        return k.get_contents_as_string()

    def setMetadata(self,bucket,key,metadataName,metadata):
        k = self.connection.get_bucket(bucket).get_key(key)
        k.set_metadata(metadataName,metadata)

    def getFileList(self,bucket = None):
        if(bucket is None):
            return self.__defaultBucket.list()
        
        for key in bucket:
            pass

    def createFolder(self,name,bucket=None,pathToFolder=""):
        if(bucket is None):
            k = Key(self.__defaultBucket)
        else:
            k = Key(self[bucket])
        k.key = pathToFolder + name + "/"
        k.set_contents_from_string("")


    def deleteKey(self,keyName,bucket):
        if(bucket is None):
            self.__defaultBucket.delete_key(keyName)
        else:
            bucket.delete_key(keyName)

    def getMD5(self,keyName,bucket = None):
        bucket = self.__getProperBucket(bucket)
        return bucket.get_key(keyName).get_md5_from_hexdigest()

    def downloadFileURL(self,keyName,bucket = None):
        bucket = self.__getProperBucket(bucket)
        return bucket.get_key(keyName).generate_url(5)

    def getFileListAsHGrid(self,bucket = None):
        '''
        {
        'uid':X, 
        'type':"", 
        'name':"", 
        'parent_uid':Y}
        '''
        bucket = self.__getProperBucket(bucket)
        bucketList = bucket.list()
        folders = self._getFolders(bucketList)
        files = []
        parent =  {
            'uid': 0,
            'name': str(bucket.name),
            'type': 'folder',
            'parent_uid': 'null'
        }
        folders.append(parent)

        i = len(folders)



        for k in bucketList:

            s = str(k.key)
            if not s.endswith('/'):
                row = {
                'uid':0,
                'name':'null',
                'type':'null',
                'parent_uid': 0
                }
                row['name'] = s[s.rfind('/')+1:]
                row['uid'] = i
                i+=1

                row['type'] = 'file'
                d = s.split('/')
                if len(d) > 1:
                        q = (x for x in folders if x['name'] == d[len(d)-2]).next()
                        if q:
                            row['parent_uid']=q['uid']
               
                files.append(row)

        folders.extend(files)
        return folders


    def _getFolders(self,bucketList):
        folders = []
        i = 1
        for k in bucketList:

            row = {
            'uid':i,
            'name':'null',
            'type':'folder',
            'parent_uid':0
             }
        
            row['uid'] = i
            s1 = str(k.key)
            d = s1.split('/')

            for l  in d[:len(d)-1]:
                if l not in [x['name'] for x in folders]:
                    row['name']=l
                    if len(d) > 1:
                        q = (x for x in folders if x['name'] == d[len(d)-2]).next()
                        if q:
                            row['parent_uid']=q['uid']
                    folders.append(row)
                    i+=1
        return folders
        
class S3Key:
    def __init__(self, key):
        self.s3Key = key
        self.fullName = str(key.key)
        self.name = 
        if(str(key.key).endswith('/')):
            self.type = 'files'
        else:
            self.type = 'folder'
    @property
    def name(self):
        return self._nameAsStr()[self._nameAsStr().rfind('/'):]

    def _nameAsStr(self):
        return str(self.s3Key.key)
