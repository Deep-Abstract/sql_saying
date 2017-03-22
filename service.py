# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 20:39:28 2017
@author: Thautwarm
service
"""
from . import entity,dao
baseDao=dao.baseDao
User=entity.entities.user



"""
logIn Page
"""
Login_userStyle=User()
Login_userSug=User()
Login_userStyle.password='password'
Login_userStyle.username="text"
Login_userStyle.email='text'
Login_userStyle.info='text'
Login_userStyle.school='text'
Login_userSug.password='Input your password here.'
Login_userSug.username='Your username please.'
Login_userSug.email='Your email.'
Login_userSug.school='Your school?'
Login_userSug.info='Anything you want say?'

"""
signIn Page
"""
Signin_userStyle=User()
Signin_userSug=User()
Signin_userStyle.password='password'
Signin_userStyle.username="text"
Signin_userSug.password='Input your password here.'
Signin_userSug.username='Your username please.'


whenUserLogin={'hiddenAttrs':{'access','id','img'},
               'Login_userSug':Login_userSug,
               'Login_userStyle':Login_userStyle
               }
whenUserSignin={'hiddenAttrs':{'access','id','img','email','school','info'},
              'Signin_userSug':Signin_userSug,
              'Signin_userStyle':Signin_userStyle,
            }
               
def checkSafety(astr):
    if type(astr)!=str:
        return False
    return True
    
class UserSignLog:
    def __init__(self):
        self.dao=baseDao('user')

    def userSignIn(self,username,password):
        userdao=self.dao
        #    username=user.username
        #    password=user.password
        if not (checkSafety(username) and checkSafety(password)):return False #
        return userdao.select(username=username,password=password)
        
    def userLogIn(self,user):
        maps=user.toMap()
        if len(maps)!=len(user.attrs.difference(whenUserLogin['hiddenAttrs'])):
            return "userLogin_incompleteInfo"
        userdao=self.dao
        if  userdao.check(user=user):
            return "userLogin_duplicated"
        if userdao.add(user=user):
            return "userLogin_finished"
        return "userLogin--error"

    
    def userCurrent(self,username,id):
        userdao=self.dao
        selected=userdao.select(username=username,id=id)
        if len(selected)!=1:
            return None,None
        else:
            entity=selected[0]
            return entity['img'],entity['info']

    def userChangeInfo(self,**maps):
        userdao=self.dao
        if userdao.change(**maps):
            return "userChangeInfo--finished"
        else:
            return "userChangeInfo--error"
        



    
    
    
    
    
    
    
    
    
        
    
    
    
    
