Imports System.IO
Imports System.Security.Cryptography

Public Class Form1

    Function md5_hash(ByVal file_name As String)
        Return hash_generator("md5", file_name)
    End Function

    Function hash_generator(ByRef hash_type As String, ByRef file_name As String)
        Dim hash
        hash = MD5.Create

        Dim hashValue() As Byte
        Dim filestream As FileStream = File.OpenRead(file_name)
        filestream.Position = 0
        hashValue = hash.ComputeHash(filestream)
        Dim hash_hex = PrintByteArray(hashValue)

        filestream.Close()

        Return hash_hex
    End Function

    Public Function PrintByteArray(ByRef array() As Byte)
        Dim hex_value As String = ""
        Dim i As Integer
        For i = 0 To array.Length - 1
            hex_value += array(i).ToString("x2")
        Next i
        Return hex_value.ToLower
    End Function

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        If OpenFileDialog1.ShowDialog() = Windows.Forms.DialogResult.OK Then
            Dim path As String = OpenFileDialog1.FileName
            txtFilePath.Text = path

            Dim sample As String = md5_hash(path)
            txtHash.Text = sample

            Dim md5List() As String = File.ReadAllLines("md5.txt")
            If md5List.Contains(sample) Then
                lblStatus.Text = "Заражён"
                lblStatus.ForeColor = Color.Red

            Else
                lblStatus.Text = "Чист"
                lblStatus.ForeColor = Color.Green

            End If
        End If
    End Sub

    Private Sub TextBlock1_TextChanged(sender As Object, e As EventArgs) Handles txtFilePath.TextChanged

    End Sub

    Private Sub TextBox2_TextChanged(sender As Object, e As EventArgs) Handles txtHash.TextChanged

    End Sub
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load

    End Sub

    Private Sub Label1_Click(sender As Object, e As EventArgs) Handles Label1.Click

    End Sub

    Private Sub Label3_Click(sender As Object, e As EventArgs) Handles Label3.Click

    End Sub
End Class
