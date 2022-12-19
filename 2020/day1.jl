### A Pluto.jl notebook ###
# v0.12.16

using Markdown
using InteractiveUtils

# ╔═╡ 67540b50-3aa8-11eb-196b-0d302ad79dd5
md"## This part implements the 2 sum function"

# ╔═╡ 8688cfe0-3aa5-11eb-1a8b-eb51e7a9dd45
function two_sum(data_list, total=2020)
	num_items = 0
	data = Dict{Integer, Integer}()
	for value in data_list
		complement = total-value
		if haskey(data, complement)
			return (complement*data[complement])
		end
		data[value] = complement
	end
end

# ╔═╡ b74f09ae-3aa4-11eb-1f34-91f6c3d9fe0c
begin
	data_list = map(x -> parse(Int, x), split("""1721
	979
	366
	299
	675
	1456""", "\n"))
	two_sum(data_list)
end

# ╔═╡ cf613040-3aa5-11eb-17bc-1394dbbe4b9e
data_list[4:length(data_list)]

# ╔═╡ 4ec00560-3848-11eb-27fa-5f4fe5998ada
open("data\\1_input.txt") do f
	data_list = map(x -> parse(Int, x),readlines(f))
	two_sum(data_list)
end

# ╔═╡ fad87010-3aa7-11eb-380e-a7f0e544152f
md"## This part implements the 3 sum function"

# ╔═╡ 1a6c0b90-3aa7-11eb-0c0e-fbb27794740a
function three_sum(data_list, total=2020)
	num_items = length(data_list)
	data = Dict()
	for (i, v1) in enumerate(data_list)
		for v2 in data_list[i+1:num_items]
			data[v1+v2] = (v1, v2)
		end
	end
	for value in data_list
		complement = total-value
		if haskey(data, complement)
			v1, v2 = data[complement]
			return (value, v1, v2, value*v1*v2)
		end
	end
end

# ╔═╡ de82ac60-3aa6-11eb-364a-7d48ca0e25d8
three_sum(data_list)

# ╔═╡ c9a4eaf0-3aa7-11eb-03d5-73581aa42d8c
979+
366+
675

# ╔═╡ db830b80-3aa7-11eb-24aa-87d02deece39
open("data\\1_input.txt") do f
	data_list = map(x -> parse(Int, x),readlines(f))
	three_sum(data_list)
end

# ╔═╡ Cell order:
# ╟─67540b50-3aa8-11eb-196b-0d302ad79dd5
# ╠═8688cfe0-3aa5-11eb-1a8b-eb51e7a9dd45
# ╠═b74f09ae-3aa4-11eb-1f34-91f6c3d9fe0c
# ╠═cf613040-3aa5-11eb-17bc-1394dbbe4b9e
# ╠═4ec00560-3848-11eb-27fa-5f4fe5998ada
# ╟─fad87010-3aa7-11eb-380e-a7f0e544152f
# ╠═1a6c0b90-3aa7-11eb-0c0e-fbb27794740a
# ╠═de82ac60-3aa6-11eb-364a-7d48ca0e25d8
# ╠═c9a4eaf0-3aa7-11eb-03d5-73581aa42d8c
# ╠═db830b80-3aa7-11eb-24aa-87d02deece39
