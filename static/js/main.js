function isvalidUsername()
{
    var username = document.getElementById("uname").value;
    if (username.length<=4)
    {
        document.getElementById("uname_hint").style["color"] = "red";
        return false;
    }
    document.getElementById("uname_hint").style["color"] = "lime";
    return true;
}
function isValidPasskey()
{
    var hint = "Password strength is "
    var psd = document.getElementById("psd").value;
    var psdreg = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$/;
    if(!psd.match(psdreg))
    {
        document.getElementById("psd_hint").innerHTML = hint+"weak";
        document.getElementById("psd_hint").style["color"] = "red";
        return false;
    }
    document.getElementById("psd_hint").innerHTML = hint+"strong";
    document.getElementById("psd_hint").style["color"] = "lime";
    return true;
}
function cpsdMatchesPsd()
{
    var hint = "Passwords ";
    var cpsd = document.getElementById("cpsd").value;
    var psd= document.getElementById("psd").value;
    if(psd!=cpsd)
    {
        document.getElementById("cpsd_hint").style["color"]= "red";
        document.getElementById("cpsd_hint").innerHTML = hint+"didn't match!";
        return false;
    }
    document.getElementById("cpsd_hint").style["color"]= "lime";
    document.getElementById("cpsd_hint").innerHTML = hint+"matched!";
    return true;
}
function isValidMail()
{
    var hint = "Mail id is ";
    var mail = document.getElementById("mail").value;
    var mail_reg = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(!mail.match(mail_reg))
    {
        document.getElementById("mail_hint").style["color"] = "red";
        document.getElementById("mail_hint").innerHTML = hint+"invalid!";
        return false;
    }
    document.getElementById("mail_hint").style["color"] = "lime";
    document.getElementById("mail_hint").innerHTML = hint+"valid!";
    return true;
}
function validateForm()
{
    if(isvalidUsername()&&isValidMail()&&isValidPasskey()&&cpsdMatchesPsd())
    {
        return true;
    }
    return false;
}