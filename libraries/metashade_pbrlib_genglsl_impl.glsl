void mx_metashade_generalized_schlick_bsdf(float weight, vec3 color0, vec3 color90, float exponent, out vec3 result)
{
	result = color0 * weight;
}

