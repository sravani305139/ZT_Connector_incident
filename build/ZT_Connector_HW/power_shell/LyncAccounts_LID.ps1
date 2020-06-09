# Script will lookup all appropriate settings based on LID code for bulk EID's to create Lync account
# ExtensionAttribute1 determines if Full time employee and granted BIRTHRIGHTS or not
# ExtensionAttribute4 determines the site in which a user LID is
# If users LID is not in the database only they will be enabled for IM and Presence
# Created by Jeff McBride jeffrey.mcbride@honeywell.com, www.lynclead.com
# Date modified: 8/18/2016, updated DC used in AD User lookup
# Added LocationPolicies on 11/9 - Jeff
# Corrected . ".\Get First X Available DID in Range.ps1" $site.NumRangeID on 6/21 from $site.LID
# Modified Birthrights from only EA1 "m" to also include "E and C" on 9/20/2017

$starttime = get-date
$WarningPreference = "SilentlyContinue"
$Database = Import-CSV .\Lync-SiteFeaturesDatabase.csv

#[System.Collections.ArrayList]$EIDList = @()
#$TempEIDList = Get-Content .\EnableLyncAccount_EIDs.txt
#$EIDList = @($TempEIDList)

#[System.Collections.ArrayList]$EIDList2 = @()
#$TempEIDList2 = Get-Content .\EnableLyncAccount_EIDs.txt
#$EIDList2 = @($TempEIDList2)

[System.Collections.ArrayList]$FailedEnableList

try
{
$ExchangeSession = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri http://webmail.honeywell.com/PowerShell/ -Authentication Kerberos
Import-PSSession $ExchangeSession
Set-ADServerSettings -ViewEntireForest $TRUE

Write-Host ""
Write-Host "-------------------------------------------------------"
Write-Host ""



	$ADUserLookup = Get-ADUser -Server de08dc0011.ds.honeywell.com:3268 -Identity $args[7] -Properties * | select SamAccountName, ExtensionAttribute1, ExtensionAttribute4, GivenName, emailaddress
	$LID = $ADUserLookup.ExtensionAttribute4
	Write-Host $args[7] "is located at site" $LID
	$Site = $Database | ? {$_.LID -eq $LID}

	$Precheck = Get-CSUser -Identity $args[7] -ea 0
		if ($Precheck.Enabled -eq "TRUE") {
			Write-Host $args[7] "is already enabled for Lync, removing them from the enable list"
			#$EIDList2.Remove("$args[7]")
			} else {
			
				if ($Site -eq $NULL) {
					Write-Host $LID "is not identified in Database.  Only basic IM and Presence will be enabled for" $args[7]
					Write-Host $args[7] "site is not in database therefore P2P is being disabled"
					
						if ($ADUserLookup.EmailAddress -notlike "*@honeywell.com") {
							$error.clear()
							Enable-CSUser -Identity $args[7] -RegistrarPool "de08ucpool03.global.ds.honeywell.com" -SipAddressType FirstLastName -SipDomain "honeywell.com"
							if ($error[0] -like "*Management object not found*") {Write-Host "$args[7] failed to enable for Lync.  Account is likely disabled or doesn't exist, Site is Null, Email not HW"; #$EIDList2.Remove("$args[7]"); 
                            $FailedEnableList.Add("$args[7]"); continue}
							Write-Host $ADUserLookup.EmailAddress "EmailAddress domain is not @honeywell.com therefore using FirstLastName for SIP address"
							
						} else {
							$error.clear()
							Enable-CSUser -Identity $args[7] -RegistrarPool "az18ucpool03.global.ds.honeywell.com" -SipAddressType EmailAddress
							if ($error[0] -like "*Management object not found*") {Write-Host "$args[7] failed to enable for Lync.  Account is likely disabled or doesn't exist, Site is Null, Email is HW"; #$EIDList2.Remove("$args[7]");
                            $FailedEnableList.Add("$args[7]"); continue}
							Write-Host $args[7] "has been enabled for Lync in az18ucpool03.global.ds.honeywell.com"
							}
					
				} else {
						if ($ADUserLookup.EmailAddress -notlike "*@honeywell.com") {
						$error.clear()
						Write-Host $ADUserLookup.EmailAddress "EmailAddress domain is not @honeywell.com therefore using FirstLastName for SIP address"
						Enable-CSUser -Identity $args[7] -RegistrarPool $Site.RegistrarPool -SipAddressType FirstLastName -SipDomain "honeywell.com"
						if ($error[0] -like "*Management object not found*") {Write-Host "$args[7] failed to enable for Lync.  Account is likely disabled or doesn't exist, Site Exists, Email not HW"; 
                        #$EIDList2.Remove("$args[7]"); 
                        $FailedEnableList.Add("$args[7]"); continue}
						Write-Host $args[7] "has been enabled for Lync in " $Site.RegistrarPool
						}
						else {
						$error.clear()
						Enable-CSUser -Identity $args[7] -RegistrarPool $Site.RegistrarPool -SipAddressType EmailAddress
						if ($error[0] -like "*Management object not found*") {Write-Host "$args[7] failed to enable for Lync. Account is likely disabled or doesn't exist, Site Exists, Email is HW"; 
                        #$EIDList2.Remove("$EID"); 
                        $FailedEnableList.Add("$args[7]"); continue}
						Write-Host $args[7] "has been enabled for Lync in " $Site.RegistrarPool
						}
				}
			}


if ($FailedEnableList -ne $Null) {Write-Host ""; Write-Host "Following EID's have failed to be enabled and will not have their accounts further processed with the rest"; Write-Host $FailedEnableList} 

if ($args[7].count -eq 0) {Write-Host ""; Get-PSSession | Remove-PSSession; Write-Host "None of the accounts were enabled successfully.  Review account status and troubleshoot.  Exiting Script"; Write-Host ""; return}

	## All USers in list should have bare back Lync accounts enabled by now in their correct pool.
	Write-Host ""
	Write-Host "All valid users have been enabled with BASIC Lync features."
	Write-Host ""
	Write-Host "Waiting 5 minutes to allow replication before assigning users all applicable policies based on their accounts..."
	Write-Host ""
	(get-date).DateTime
	Write-Host ""
	Write-Host "-------------------------------------------------------"
	Start-Sleep -s 300
	Write-Host ""

	
	$ADUserLookup = Get-ADUser -Server de08dc0011.ds.honeywell.com:3268 -Identity $args[7] -Properties * | select SamAccountName, ExtensionAttribute1, ExtensionAttribute4, GivenName, emailaddress
	$LID = $ADUserLookup.ExtensionAttribute4
	$GivenName = $ADUserLookup.GivenName
	$Email2 = "dl-wiprolyncteam@honeywell.com"
	$Email = $ADUserLookup.emailaddress
	$EmpStatTemp = $ADUserLookup.ExtensionAttribute1
		if ($EmpStatTemp -match "M|C|E") {$Birthrights = "YES"} else {$Birthrights = "NO"}
	
	Write-Host ""
	Write-Host $args[7] "is located at site" $LID
	Write-Host "Birthrights status for" $args[7] "are" $Birthrights
	$Site = $Database | ? {$_.LID -eq $LID}
	
#### LID Not in Database only assign IM & PRESENCE
	if ($Site -eq $NULL) {
	Write-Host $LID "is not identified in Database.  Only basic IM and Presence will be enabled for" $args[7]
				
		#Step 0b: Set AudioVideoDisabled
		Set-CSUser -Identity $args[7] -AudioVideoDisabled $TRUE
		Write-Host $args[7] "site is not in database therefore P2P is being disabled"
	}
	
#### LID within Database and OK to move forward with feature lookup
	
	else {
	Write-Host $Site.LID "is within LID Code database"
	Write-Host "The following features were identified for" $LID
	$Site

#####################   Full Employee Granting complete LID Birthrights

	if ($Birthrights -eq "YES") {

	
		#Step 2: Set AudioVideoDisabled
		if ($Site.AudioVideoDisabled -eq "TRUE") {
			Set-CSUser -Identity $args[7] -AudioVideoDisabled $TRUE
			Write-Host $args[7] "Not permitted for P2P"
			}
			else {
			Write-Host $args[7] "has been enabled for P2P"
			Set-CSUser -Identity $args[7] -AudioVideoDisabled $FALSE
			}
			
		#Step 3: Set Conferencing Policy
		Grant-CSConferencingPolicy -Identity $args[7] -PolicyName $Site.ConferencingPolicy
		Write-Host $Site.ConferencingPolicy "has been applied for" $args[7]

		#Step 4: Set Client Policy
		if ($site.ClientPolicy -ne "") {
			Grant-CSClientPolicy -Identity $args[7] -PolicyName $Site.ClientPolicy
			Write-Host $Site.ClientPolicy "has been applied for" $args[7]
			}
			else {
			Write-Host "Global client policy will be assigned by default"
			}
				
		#Step 5: Set Archiving Policy
		if ($site.ArchivingPolicy -ne "") {
			Grant-CSArchivingPolicy -Identity $args[7] -PolicyName $Site.ArchivingPolicy
			Write-Host $Site.ArchivingPolicy "has been applied for" $args[7]
			}
			else {
			Write-Host "Global Archiving Policy will be assigned by default"
			}
				
		#Step 6: Set External Access Policy
		if ($site.ExternalAccessPolicy -ne "") {
			Grant-CSExternalAccessPolicy -Identity $args[7] -PolicyName $Site.ExternalAccessPolicy
			Write-Host $Site.ExternalAccessPolicy "has been applied for" $args[7]
			}
			else {
			Write-Host "Global External Access Policy will be assigned by default"
			}
			
		#Step 8: Enterprise Voice
		if ($Site.EnterpriseVoiceEnabled -eq "TRUE") {
			. ".\Get First X Available DID in Range.ps1" $site.NumRangeID 1
			$EVNumber = $SelectDID.InputObject
			$EVNumberString = $EVNumber -as [string]
			$Last4EVNumber = $EVNumberString.Substring($EVNumberString.Length -4,4)
			$NewLineURI = "tel:+$EVNumber;ext=$Last4EVNumber"
			Set-CSUser -Identity $args[7] -EnterpriseVoiceEnabled $TRUE -LineURI $NewLineURI
			Grant-CSDialPlan -Identity $args[7] -PolicyName $Site.DialPlan
			Grant-CSVoicePolicy -Identity $args[7] -PolicyName $Site.VoicePolicy
			
			##Location Policy
			If ($Site.LocationPolicy -ne $null) {Grant-CSLocationPolicy -Identity $args[7] -PolicyName $Site.LocationPolicy}
			
			Write-Host "Enabled EV for" $args[7] "with policies" $Site.DialPlan $Site.Voicepolicy
			Enable-UMMailbox -Identity $args[7] -UMMailboxPolicy $Site.UMMailboxPolicy -Extensions $Last4EVNumber

			Write-Host ""
			Write-Host "EV has been enabled, waiting 180 seconds before moving on to ensure replication of DID shows as in use"
			Start-Sleep -s 180
			
			
		###### SEND EMAIL AFTER EVERYTHING IS CONFIGURED
				$CSUser = Get-CSUser -Identity $args[7]
				$SIPAddress = $CSUser.SipAddress.TrimStart("sip:")
				$TempNumber = $CSUser.LineURI.Split(':')
				$TemperNumber = $TempNumber[1].Split(';')
				$PhoneNumber = $TemperNumber[0]
				$Subject = "Honeywell IT Service Update:  Microsoft Skype for Business with Enterprise Voice"
				$Body = "
				<html><body>
				<font face='Arial' color='gray'>
				<b>Honeywell IT</b> <font color='red'>|</font> SERVICE UPDATE
				<br><br>
				<font size='2'>
				<i>No Action Required
				<br>
				This is an automated message.  Please do not reply.</i>
				<br><br><br>
				Hello $GivenName,
				<br><br>
				You have been enabled with Microsoft Skype for Business including all standard features available to your site, <a href='https://teamsites2013.honeywell.com/sites/UnifiedCollaboration/lync/Lists/Lync%20Features%20by%20LID/AllItems.aspx'>click here</a> to view the available features by locating your LID code.
				<br><br>  
				Your sign on address is $SIPAddress and Enterprise Voice phone number is $PhoneNumber which allows you to utilize your client as a telephone including voicemail services.
				<br><br>
				Instructor led training, video snippets and reference articles can be found at:  <a href='https://quickhelp.com/honeywell/#/topics/381/categories/6276/assets'>Getting Started with Skype for Business</a>.
				<br><br>
				<a href='https://teamsites2013.honeywell.com/sites/UnifiedCollaboration/lync/Skype%20for%20Business%20Client/Skype%20for%20Business%20Guide.pdf'>Click here</a> for the Microsoft Skype for Business User Guide.
				<br><br>
				Contact the Honeywell IT Service Desk for any issues or concerns.
				<br><br>
				Thanks,
				<br>
				Honeywell Enterprise IT | Unified Collaboration
				</font></font>
				</body></html>
				"	
				Send-MailMessage -from "SkypeService_DoNotReply@honeywell.com" -to $EMail -bcc $Email2 -SmtpServer 'smtp-secure.honeywell.com' -Subject $Subject -BodyAsHTML $body
			###### END EMAIL 
			}
		else {
			Write-Host "Unable to enable EV since the site is not permitted"
			
					###### SEND EMAIL Birthrights but no EV at site
				$SIPAddress = ((Get-CSUser -Identity $args[7]).SipAddress).TrimStart("sip:")
				$Subject = "Honeywell IT Service Update:  Microsoft Skype for Business"
				$Body = "
				<html><body>
				<font face='Arial' color='gray'>
				<b>Honeywell IT</b> <font color='red'>|</font> SERVICE UPDATE
				<br><br>
				<font size='2'>
				<i>No Action Required
				<br>
				This is an automated message.  Please do not reply.</i>
				<br><br><br>
				Hello $GivenName,
				<br><br>
				You have been enabled with Microsoft Skype for Business including all standard features available to your site, <a href='https://teamsites2013.honeywell.com/sites/UnifiedCollaboration/lync/Lists/Lync%20Features%20by%20LID/AllItems.aspx'>click here</a> to view the available features by locating your LID code.
				<br><br>  
				Your sign on address is $SIPAddress 
				<br><br>
				Instructor led training, video snippets and reference articles can be found at:  <a href='https://quickhelp.com/honeywell/#/topics/381/categories/6276/assets'>Getting Started with Skype for Business</a>.
				<br><br>
				<a href='https://teamsites2013.honeywell.com/sites/UnifiedCollaboration/lync/Skype%20for%20Business%20Client/Skype%20for%20Business%20Guide.pdf'>Click here</a> for the Microsoft Skype for Business User Guide.
				<br><br>
				Contact the Honeywell IT Service Desk for any issues or concerns.
				<br><br>
				Thanks,
				<br>
				Honeywell Enterprise IT | Unified Collaboration
				</font></font>
				</body></html>
				"		
				Send-MailMessage -from "SkypeService_DoNotReply@honeywell.com" -to $EMail -bcc $Email2 -SmtpServer 'smtp-secure.honeywell.com' -Subject $Subject -BodyAsHTML $body
			###### END EMAIL
			}	
	}


	########## NO BIRTH RIGHTS
	ELSE
	{
		#Step 2a: Set AudioVideoDisabled
		if ($Site.AudioVideoDisabled -eq "TRUE") {
			Set-CSUser -Identity $args[7] -AudioVideoDisabled $TRUE
			Write-Host $args[7] "Not permitted for P2P"
			}
			else {
			Write-Host $args[7] "has been enabled for P2P"
			Set-CSUser -Identity $args[7] -AudioVideoDisabled $FALSE
			}
			
		#Step 3a: Set Conferencing Policy
		Grant-CSConferencingPolicy -Identity $args[7] -PolicyName $Site.ConferencingPolicy
		Write-Host $Site.ConferencingPolicy "has been applied for" $args[7]

		#Step 4a: Set Client Policy
		if ($site.ClientPolicy -ne "") {
			Grant-CSClientPolicy -Identity $args[7] -PolicyName $Site.ClientPolicy
			Write-Host $Site.ClientPolicy "has been applied for" $args[7]
			}
			else {
			Write-Host "Global client policy will be assigned by default"
			}
				
		#Step 5a: Set Archiving Policy
		if ($site.ArchivingPolicy -ne "") {
			Grant-CSArchivingPolicy -Identity $args[7] -PolicyName $Site.ArchivingPolicy
			Write-Host $Site.ArchivingPolicy "has been applied for" $args[7]
			}
			else {
			Write-Host "Global Archiving Policy will be assigned by default"
			}
				
		#Step 6a: Set External Access Policy
		if ($site.ExternalAccessPolicy -ne "") {
			Grant-CSExternalAccessPolicy -Identity $args[7] -PolicyName $Site.ExternalAccessPolicy
			Write-Host $Site.ExternalAccessPolicy "has been applied for" $args[7]
			}
			else {
			Write-Host "Global External Access Policy will be assigned by default"
			}
			
			###### SEND EMAIL No Birthrights
				$SIPAddress = ((Get-CSUser -Identity $args[7]).SipAddress).TrimStart("sip:")
				$Subject = "Honeywell IT Service Update:  Microsoft Skype for Business"
				$Body = "
				<html><body>
				<font face='Arial' color='gray'>
				<b>Honeywell IT</b> <font color='red'>|</font> SERVICE UPDATE
				<br><br>
				<font size='2'>
				<i>No Action Required
				<br>
				This is an automated message.  Please do not reply.</i>
				<br><br><br>
				Hello $GivenName,
				<br><br>
				You have been enabled with Microsoft Skype for Business including all standard features available to your site, <a href='https://teamsites2013.honeywell.com/sites/UnifiedCollaboration/lync/Lists/Lync%20Features%20by%20LID/AllItems.aspx'>click here</a> to view the available features by locating your LID code.
				<br><br>  
				Your sign on address is $SIPAddress 
				<br><br>
				Instructor led training, video snippets and reference articles can be found at:  <a href='https://quickhelp.com/honeywell/#/topics/381/categories/6276/assets'>Getting Started with Skype for Business</a>.
				<br><br>
				<a href='https://teamsites2013.honeywell.com/sites/UnifiedCollaboration/lync/Skype%20for%20Business%20Client/Skype%20for%20Business%20Guide.pdf'>Click here</a> for the Microsoft Skype for Business User Guide.
				<br><br>
				Contact the Honeywell IT Service Desk for any issues or concerns.
				<br><br>
				Thanks,
				<br>
				Honeywell Enterprise IT | Unified Collaboration
				</font></font>
				</body></html>
				"		
				Send-MailMessage -from "SkypeService_DoNotReply@honeywell.com" -to $EMail -bcc $Email2 -SmtpServer 'smtp-secure.honeywell.com' -Subject $Subject -BodyAsHTML $body
			###### END EMAIL
				
		}
	}
	Write-Host ""
	Write-Host "$args[7] account created and email sent."
	Write-Host ""
	Write-Host "-------------------------------------------------------"
	



Get-PSSession | Remove-PSSession
$endtime = get-date
$timeoutput = ($endtime - $starttime)
write-host "Time to run this script: $timeoutput"
$path = "./Queue/executing_files/"

$name = $args[2] + ".txt"
New-Item -Path $path -Name $name -ItemType File 

$args[2] | Out-File -FilePath $path -Append -Force -ErrorAction SilentlyContinue
$args[5] | Out-File -FilePath $path -Append -Force -ErrorAction SilentlyContinue

"Executed" | Out-File -FilePath $path -Append -Force -ErrorAction SilentlyContinue

}

catch
{
$path = "./Queue/executing_files/"

$name = $args[2] + ".txt"
New-Item -Path $path -Name $name -ItemType File 

$args[2] | Out-File -FilePath $path -Append -Force -ErrorAction SilentlyContinue
$args[5] | Out-File -FilePath $path -Append -Force -ErrorAction SilentlyContinue

"reassign_group" | Out-File -FilePath $path -Append -Force -ErrorAction SilentlyContinue

}