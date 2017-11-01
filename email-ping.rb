#!/usr/bin/env ruby
#
# = Email Ping
#
# Check to see if an email address exists by looking up MX records and connecting
# to the address's home SMTP server. It then starts to send a message to the address
# but quits before the message is actually sent.

require 'resolv'
require 'net/smtp'

address = ARGV[0].chomp
domain = address.split('@').last
dns = Resolv::DNS.new

puts "Resolving MX records for #{domain}..."
mx_records = dns.getresources domain, Resolv::DNS::Resource::IN::MX
mx_server  = mx_records.first.exchange.to_s
puts "Connecting to #{mx_server}..."

Net::SMTP.start mx_server, 25 do |smtp|
  smtp.helo "loldomain.com"
  smtp.mailfrom "test@loldomain.com"

  puts "Pinging #{address}..."

  puts "-" * 50

  begin
    smtp.rcptto address
    puts "Address probably exists."
  rescue Net::SMTPFatalError => err
    puts "Address probably doesn't exist."
  end
end
