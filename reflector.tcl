#!/usr/bin/tclsh

set listen_port 0
set server_port 00
set server ""
while {[llength $argv]>0} {
 switch -- [lindex $argv 0] {
    -l  { set listen_port [lindex $argv 1] 
          set argv [lrange $argv 2 end]
          continue
        }
    -s  { set server [lindex $argv 1]
          set argv [lrange $argv 2 end]
          continue
        }
    -p  { set server_port [lindex $argv 1]
          set argv [lrange $argv 2 end]
          continue
        }
 }
 puts stderr "Unknown option [lindex $argv 0]\r"
 exit 1
}

if {$listen_port == 0} {
  puts stderr "Must use -l to set listen port"
  exit 1
}

if {[string equal "" "$server"]} {
  puts stderr "Must use -s to set server"
  exit 1
}

if {$server_port == 0} {
  puts stderr "Must use -p to set server port"
  exit 1
}

proc relay {from to stdoutmarker} {
  set data [read $from]
  set data [regsub -nocase "sm9.ifost.local:13080" $data "192.168.56.1:13080"]
  set data [regsub -nocase "sm9:13080" $data "192.168.56.1:13080"]
  puts -nonewline $to $data
  puts -nonewline stdout $data
#  set lines [split $data "\n"]
#  puts -nonewline $stdoutmarker
#  puts [join $lines "\n$stdoutmarker"]
#  if {[eof $from]} { 
#   close $from
#   close $to
#   puts "\[\[<<EOF>>\]\]"
#  }
}

proc accept_connection {new_channel connecting_host connecting_port} {
 global server
 global server_port
 set remote [socket $server $server_port]
 set local $new_channel
 fconfigure $local -blocking no -buffering none
 fconfigure $remote -blocking no -buffering none
 fileevent $local readable  [list relay $local  $remote "+> "]
 fileevent $remote readable [list relay $remote $local "<+ "]
}

set local_socket [socket -server accept_connection $listen_port]
fconfigure stdout -buffering none
vwait forever
