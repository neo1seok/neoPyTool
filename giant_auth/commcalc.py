import neolib.neoutil as neolib
import hashlib

def HexStrSubStr(org, index, count):
	return org[2 * index:2 * (index + count)]


def DeriveKey(MasterKey, sectorID, SN):
	if len(SN) != 9 * 2:
		return "";

	SN01 = HexStrSubStr(SN, 0, 2);
	SN8 = HexStrSubStr(SN, 8, 1);

	shaInput = MasterKey + "1C" + "04" + sectorID + SN8 + SN01 + ZeroHexStr(48) + SN;
	return SHA256(shaInput)


def ZeroHexStr(count):
	return "00" * count;


def CalcMAC(key, strChallenge, sectorID, SN):
	if len(SN) != 9 * 2:
		return "";

	SN01 = HexStrSubStr(SN, 0, 2)
	SN23 = HexStrSubStr(SN, 2, 2)
	SN47 = HexStrSubStr(SN, 4, 4)
	SN8 = HexStrSubStr(SN, 8, 1)

	Zero11 = "0000000000000000000000";

	shaInput = key + strChallenge + "0840" + sectorID + Zero11 + SN8 + SN47 + SN01 + SN23;

	return SHA256(shaInput)


def SHA256(shaInput):
	m = hashlib.sha256()
	m.update(neolib.HexString2ByteArray(shaInput))
	reshash = m.digest()

	return neolib.ByteArray2HexString(reshash)


def CalcMamFromMasterKey(self, challenge, masterKey):
	sn = "4C4715000000000047"
	# challenge = "2F9005AE9C1F0662E88DBA4DEE582A601547AE3F83005C3C4F26FF9C21FAD2C5"
	derifiedKey = DeriveKey(masterKey, "0000", sn)
	mac = CalcMAC(derifiedKey, challenge, "0000", sn)
	print(mac)
	return mac