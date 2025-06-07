from utils import Annotation

@Annotation.func_desc("这是配置headers,params,cookies的类")
class JsonParametersConfig():
    def __init__(self):
        self.video_headers = {
    
}
        self.video_cookies = {
    
}

        self.live_video_params = {
   
}
        self.live_video_headers = {
    
}
   

        self.__video_list_url = 'https://www.douyin.com/aweme/v1/web/aweme/post/'
        self.video_list_params = {
          
      }
        self.__video_list_headers = {
          
      }
        
        self.__video_list_cookies = {
    

        }

    def get_video_headers(self):
        return self.video_headers

    def set_video_headers(self, value):
        self.video_headers = value

    def get_video_cookies(self):
        return self.video_cookies

    def set_video_cookies(self, value):
        self.video_cookies = value

    @property
    def _video_list_url(self):
        return self.__video_list_url

    @_video_list_url.setter
    def _video_list_url(self, value):
        self.__video_list_url = value

    def get_video_list_params(self):
        return self.video_list_params

    def set_video_list_params(self, value):
        self.video_list_params = value

    @property
    def _video_list_headers(self):
        return self.__video_list_headers

    @_video_list_headers.setter
    def _video_list_headers(self, value):
        self.__video_list_headers = value

    @property
    def _video_list_cookies(self):
        return self.__video_list_cookies

    @_video_list_cookies.setter
    def _video_list_cookies(self, value):
        self.__video_list_cookies = value