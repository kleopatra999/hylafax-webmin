# arrays for configuration parameters

@hylaParams=("PageSize", "VRes", "JobFmt", "RcvFmt", "DateFormat");

@commParams=("AreaCode", "CountryCode", "InternationalPrefix", "LongDistancePrefix",
	"MaxConcurrentJobs", "MaxDials", "MaxSendPages", "MaxTries"); 
	
@modemParams=("AreaCode", "CountryCode", "LongDistancePrefix", "InternationalPrefix", 
	"FAXNumber", "LocalIdentifier", "TagLineFormat", "SpeakerVolume", "ModemDialCmd", 
	"MaxRecvPages", "RingsBeforeAnswer", "JobReqBusy", "JobReqNoAnswer", "JobReqNoCarrier");
	
%defaults=("AreaCode"=>"none", "CountryCode"=>"none", "DateFormat"=>"none",
	"FAXNumber"=>"none", "InternationalPrefix"=>"none", "JobReqBusy"=>180, 
	"JobReqNoAnswer"=>300, "JobReqNoCarrier"=>300, "LocalIdentifier"=>"none", 
	"LongDistancePrefix"=>"none", "PageSize"=>"", "MaxConcurrentJobs"=>1, 
	"MaxDials"=>12, "MaxSendPages"=>"&infin;", "MaxRecvPages"=>"&infin;", 
	"MaxTries"=>3, "ModemDialCmd"=>"", "RingsBeforeAnswer"=>0, "SpeakerVolume"=>"quiet", 
	"TagLineFormat"=>'From %%n|%c|Page %%P of %%T', "VRes"=>98);

%types=("AreaCode"=>"N", "CountryCode"=>"N", "DateFormat"=>"F", "FAXNumber"=>"S", 
	"InternationalPrefix"=>"N", "JobReqBusy"=>"N", "JobReqNoAnswer"=>"N", 
	"JobReqNoCarrier"=>"N", "LocalIdentifier"=>"S", "LongDistancePrefix"=>"N", 
	"MaxConcurrentJobs"=>"N", "MaxDials"=>"N", "MaxSendPages"=>"N", "MaxRecvPages"=>"N", 
	"MaxTries"=>"N", "ModemDialCmd"=>"T", "PageSize"=>"F", "RingsBeforeAnswer"=>"N", 
	"SpeakerVolume"=>"F", "TagLineFormat"=>"F", "VRes"=>"F", "JobFmt"=>"F",
	"RcvFmt"=>"F" );