import time

banner = """
\033[1;34m                                                      
                    .:.        .:,                    
                   xM;           XK.                  
                  dx'            .lO.                 
                 do                ,0.                
             .c.lN'      ,  '.     .k0.:'             
              xMMk;d;''cOM0kWXl,',locMMX.             
              .NMK.   :WMMMMMMMx    dMMc              
               lMMO  lWMMMMMMMMMO. lMMO               
                cWMxxMMMMMMMMMMMMKlWMk                
                 .xWMMMMMMMMMMMMMMM0,\033[1;36m                 
                   .,OMd,,,;0MMMO,.                   
             .l0O.\033[1;37mVXVX\033[1;36mOX\033[1;37mVXVX\033[1;36m0MO\033[1;37mVXVX\033[1;36m.0Kd,             
            lWMMO0\033[1;37mVXVX0\033[1;36mOX\033[1;37mVXVX\033[1;36ml\033[1;37mVXVX\033[1;36m.VXNMMO            
           .MMX;.N0\033[1;37mVXVX0\033[1;36m0X\033[1;37mVXVXVX0\033[1;36m.0M:.OMMl           
          .OXc  ,MMO\033[1;37mVXVX0\033[1;36mVX\033[1;37m .VXVX0\033[1;36m0MMo  ,0X'          
          0x.  :XMMMk\033[1;37mVXVX\033[1;36m.XO\033[1;37mVXVX\033[1;36mdMMMWo.  :X'         
         .d  'NMMMMMMk\033[1;37mVXVX\033[1;36m..\033[1;37mVXVX0\033[1;36m.XMMMMWl  ;c         
            'NNoMMMMMMx\033[1;37mVXVXVXVXVX0\033[1;36m.\033[1;37mXMMk0Mc            
           .NMx OMMMMMMd\033[1;37mVXVXVX\033[1;36ml\033[1;37mVXVX\033[1;36m.NW.;MMc           
          :NMMd .NMMMMMMd\033[1;37mVXVX\033[1;36mdMd,,,,oc ;MMWx          
          .0MN,  'XMMMMMMo\033[1;37mVX\033[1;36moMMMMMMWl   0MW,          
           .0.    .xWMMMMM:lMMMMMM0,     kc           
            ,O.     .:dOKXXXNKOxc.      do            
             '0c        -VulnX-       ,Ol             
               ;.                     :. 
"""
print(banner)
so_dien_thoai = input("Nhập số điện thoại cần spam: ")
so_lan_spam = input("Nhập số lần spam: ")

print("\nĐang khởi động tool spam...")
time.sleep(1)
print(f"Chuẩn bị spam số {so_dien_thoai} {so_lan_spam} lần...")
time.sleep(2)
print("\nTool đang được hoàn thiện, vui lòng thử lại sau vài ngày. 😅")

