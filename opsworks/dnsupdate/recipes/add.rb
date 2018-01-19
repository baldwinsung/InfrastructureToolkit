Chef::Log.level = :debug


require 'rubygems'
        chef_gem "aws-sdk" do
        compile_time true
        action :install
        end

include_recipe "route53"

instance = search("aws_opsworks_instance","self:true").first

route53_record "create a record" do
  name 			"#{instance['hostname']}" + "#{node[:custom_domain]}"
  value 		"#{instance['private_ip']}"
  type  		"A"
  ttl   		60
  zone_id               node[:dns_zone_id]
  aws_access_key_id     node[:custom_access_key]
  aws_secret_access_key node[:custom_secret_key]
  overwrite 		true
  action 		:create
end

