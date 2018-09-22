err-remind
=============

This is my personal fork of err-reminders. I fixed various bugs and added persistent memory
(With my patches errbot will remember your reminders even after you restart errbot)

[Original Code Repository](https://github.com/kdknowlton/err-reminders.git)

I usually use sr.ht to develop. Please send patches to my email (anjan@momi.ca).
[sr.ht repository](https://git.sr.ht/~anjan/err-reminders)

ErrBot plugin to get and set scheduled reminders over chat.  
You NEED to change the locale, if you are not from germany.  

Basic Usage:  
!remind me \<when\> -> \<what\>  

Example:
!remind me tomorrow 11:00 -> Cook coffee.  
!remind me next Friday -> Party hard.

Example Output:  
Hello \<nick\>, here is your reminder: \<text\>

You can your own locale that stuff like "tommorow" "next week" etc work in your language.  

### Thanks to:  

* benjumanji
* Djiit 
* gbin
* kdknowlton (idea & first code)